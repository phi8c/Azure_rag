import io
import unittest
from pathlib import Path
from unittest.mock import AsyncMock, patch
from uuid import uuid4

from fastapi import HTTPException, UploadFile

from app.api.v1.contract_router import (
    analyze_contract_advanced,
    analyze_contract_advanced_company_rule,
    analyze_contract_advanced_legal,
)
from app.schemas.contract_advanced_request import (
    ContractLegalCheck,
    ContractLegalReviewRequest,
)
from app.services.contract.contract_advanced_service import (
    ContractAdvancedService,
)


class ContractAdvancedRouterTest(unittest.IsolatedAsyncioTestCase):

    async def test_temporary_file_is_removed(self):
        observed_path = None

        async def analyze(
            service,
            db,
            file_path,
            model_id,
        ):
            nonlocal observed_path
            observed_path = Path(file_path)
            self.assertTrue(observed_path.is_file())
            self.assertEqual(
                observed_path.read_bytes(),
                b"contract",
            )
            return {
                "company_rule_review": {"results": []},
                "legal_review": {"results": []},
            }

        upload = UploadFile(
            filename="contract.pdf",
            file=io.BytesIO(b"contract"),
        )

        with patch.object(
            ContractAdvancedService,
            "analyze",
            new=analyze,
        ):
            result = await analyze_contract_advanced(
                file=upload,
                model_id=uuid4(),
                db=None,
            )

        self.assertEqual(result["legal_review"], {"results": []})
        self.assertIsNotNone(observed_path)
        self.assertFalse(observed_path.exists())

    async def test_unsupported_file_type_is_rejected(self):
        upload = UploadFile(
            filename="contract.txt",
            file=io.BytesIO(b"contract"),
        )

        with self.assertRaises(HTTPException) as error:
            await analyze_contract_advanced(
                file=upload,
                model_id=uuid4(),
                db=None,
            )

        self.assertEqual(error.exception.status_code, 400)

    async def test_company_rule_endpoint_removes_temporary_file(self):
        observed_path = None

        async def analyze_company_rule(
            service,
            db,
            file_path,
            model_id,
        ):
            nonlocal observed_path
            observed_path = Path(file_path)
            self.assertTrue(observed_path.is_file())
            return {
                "company_rule_review": {"results": []},
                "legal_checks": [],
            }

        upload = UploadFile(
            filename="contract.docx",
            file=io.BytesIO(b"contract"),
        )

        with patch.object(
            ContractAdvancedService,
            "analyze_company_rule",
            new=analyze_company_rule,
        ):
            result = await analyze_contract_advanced_company_rule(
                file=upload,
                model_id=uuid4(),
                db=None,
            )

        self.assertEqual(result["legal_checks"], [])
        self.assertFalse(observed_path.exists())

    async def test_legal_endpoint_passes_handoff_data(self):
        model_id = uuid4()
        request = ContractLegalReviewRequest(
            model_id=model_id,
            legal_checks=[
                ContractLegalCheck(
                    contract_text="Clause",
                    metadata_seeds={"title": ["contract"]},
                )
            ],
        )

        with patch.object(
            ContractAdvancedService,
            "analyze_legal",
            new=AsyncMock(
                return_value={"legal_review": {"results": []}}
            ),
        ) as analyze_legal:
            result = await analyze_contract_advanced_legal(
                request=request,
                db=None,
            )

        analyze_legal.assert_awaited_once_with(
            db=None,
            model_id=model_id,
            legal_checks=[
                {
                    "contract_text": "Clause",
                    "metadata_seeds": {"title": ["contract"]},
                }
            ],
        )
        self.assertEqual(result, {"legal_review": {"results": []}})
