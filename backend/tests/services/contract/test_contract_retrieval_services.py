import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import duckdb

from app.core.settings import settings
from app.services.azure.azure_search_service import (
    AzureSearchService,
)
from app.services.contract.company_policy_retrieval_service import (
    CompanyPolicyRetrievalService,
)
from app.services.contract.legal_retrieval_service import (
    LegalRetrievalService,
)


class CompanyPolicyRetrievalServiceTest(
    unittest.IsolatedAsyncioTestCase
):

    async def test_empty_checks_do_not_call_azure_search(self):
        with patch.object(
            AzureSearchService,
            "retrieve_contract_policy",
        ) as retrieve:
            result = await CompanyPolicyRetrievalService.retrieve([])

        self.assertEqual(result, [])
        retrieve.assert_not_called()

    async def test_empty_context_preserves_company_check(self):
        with patch.object(
            AzureSearchService,
            "retrieve_contract_policy",
            return_value=[],
        ):
            result = await CompanyPolicyRetrievalService.retrieve(
                [
                    {
                        "contract_text": "Clause A",
                        "retrieval_seeds": ["approval"],
                    }
                ]
            )

        self.assertEqual(
            result,
            [{"contract_text": "Clause A", "contexts": []}],
        )

    async def test_uses_one_seed_top_one_and_preserves_mapping(self):
        first_context = {
            "chunk_id": "chunk-1",
            "parent_id": "document-1",
            "content": "Policy A",
        }
        second_context = {
            "chunk_id": "chunk-2",
            "parent_id": "document-2",
            "content": "Policy B",
        }

        def retrieve_policy(*, question, top_k):
            self.assertEqual(top_k, 1)
            return {
                "approval": [first_context],
                "authority": [second_context],
            }[question]

        with patch.object(
            AzureSearchService,
            "retrieve_contract_policy",
            side_effect=retrieve_policy,
        ) as retrieve:
            result = await CompanyPolicyRetrievalService.retrieve(
                [
                    {
                        "contract_text": "Clause A",
                        "retrieval_seeds": ["approval", "ignored"],
                    },
                    {
                        "contract_text": "Clause B",
                        "retrieval_seeds": ["authority", "ignored"],
                    },
                ]
            )

        self.assertEqual(retrieve.call_count, 2)
        self.assertEqual(
            result,
            [
                {
                    "contract_text": "Clause A",
                    "contexts": [first_context],
                },
                {
                    "contract_text": "Clause B",
                    "contexts": [second_context],
                },
            ],
        )


class LegalRetrievalServiceTest(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = Path(self.temp_dir.name) / "legal.duckdb"
        connection = duckdb.connect(str(self.db_path))
        connection.execute(
            """
            CREATE TABLE legal_documents (
                row_index BIGINT,
                document_id VARCHAR,
                vn_text VARCHAR,
                en_text VARCHAR,
                metadata JSON,
                created_at TIMESTAMP
            )
            """
        )
        connection.execute(
            """
            INSERT INTO legal_documents
            VALUES (?, ?, ?, ?, CAST(? AS JSON), CURRENT_TIMESTAMP)
            """,
            [
                1,
                "law-1",
                "Rules for commercial contract penalties.",
                None,
                json.dumps(
                    {
                        "doc_type": "Law",
                        "legal_area": "Commercial contracts",
                        "title": "Contract penalties",
                    }
                ),
            ],
        )
        connection.close()

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_empty_checks_do_not_open_database(self):
        with patch.object(
            settings,
            "LEGAL_DB_PATH",
            "missing.duckdb",
        ):
            self.assertEqual(
                LegalRetrievalService.retrieve([]),
                [],
            )

    def test_local_duckdb_returns_ranked_document(self):
        with patch.object(
            settings,
            "LEGAL_DB_PATH",
            str(self.db_path),
        ):
            result = LegalRetrievalService.retrieve(
                [
                    {
                        "contract_text": "Penalty clause",
                        "metadata_seeds": {
                            "title": ["contract penalties"],
                        },
                    }
                ]
            )

        self.assertEqual(
            result[0]["contexts"][0]["document_id"],
            "law-1",
        )

    def test_empty_context_preserves_legal_check(self):
        with patch.object(
            settings,
            "LEGAL_DB_PATH",
            str(self.db_path),
        ):
            result = LegalRetrievalService.retrieve(
                [
                    {
                        "contract_text": "Unknown clause",
                        "metadata_seeds": {
                            "title": ["zzzz-no-match"],
                        },
                    }
                ]
            )

        self.assertEqual(
            result,
            [
                {
                    "contract_text": "Unknown clause",
                    "contexts": [],
                }
            ],
        )

    def test_unknown_metadata_field_is_ignored(self):
        normalized = LegalRetrievalService._normalize_seeds(
            {
                "unknown_sql_field": ["untrusted"],
                "title": ["contract"],
            }
        )

        self.assertEqual(
            normalized,
            {"title": ["contract"]},
        )
