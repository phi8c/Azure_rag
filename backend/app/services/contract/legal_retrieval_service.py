import json
from pathlib import Path
from time import perf_counter
from typing import Any

import duckdb

from app.core.contract_advanced_logging import (
    contract_advanced_logger as logger,
)
from app.core.settings import settings


class LegalRetrievalService:

    LEGAL_TOP_K = 1
    FTS_SCHEMA = "fts_main_legal_search"

    SUPPORTED_METADATA_FIELDS = {
        "doc_type",
        "doc_number",
        "year",
        "issuer",
        "issuer_kind",
        "tier",
        "tier_name",
        "legal_area",
        "section",
        "title",
        "source",
        "url",
        "issue_date",
        "effective_date",
        "status",
        "update_date",
        "signer",
        "issuing_body",
        "parent_acts",
        "article_titles",
        "citations",
    }

    @classmethod
    def retrieve(
        cls,
        legal_checks: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:

        if not legal_checks:
            return []

        db_path = Path(
            settings.LEGAL_DB_PATH
        ).expanduser()

        if not db_path.is_absolute():
            backend_dir = Path(
                __file__
            ).resolve().parents[3]
            db_path = backend_dir / db_path

        db_path = db_path.resolve()

        if not db_path.is_file():
            raise FileNotFoundError(
                f"Legal DuckDB not found: {db_path}"
            )

        connection = duckdb.connect(
            str(db_path),
            read_only=True,
        )

        try:
            total_started_at = perf_counter()
            cls._load_and_validate_fts(connection)
            ranked_ids_by_check = []
            fts_duration = 0.0

            for check_index, check in enumerate(
                legal_checks,
                start=1,
            ):
                started_at = perf_counter()
                logger.info(
                    "[CONTRACT_ADVANCED] legal_retrieval started "
                    "check=%d/%d contract_text=%s",
                    check_index,
                    len(legal_checks),
                    check["contract_text"],
                )
                document_ids = cls._search_document_ids(
                    connection=connection,
                    metadata_seeds=check.get(
                        "metadata_seeds",
                        {},
                    ),
                )
                query_duration = perf_counter() - started_at
                fts_duration += query_duration
                logger.info(
                    "[CONTRACT_ADVANCED] legal_retrieval completed "
                    "check=%d/%d in %.3fs result_count=%d",
                    check_index,
                    len(legal_checks),
                    query_duration,
                    len(document_ids),
                )
                ranked_ids_by_check.append(
                    document_ids
                )

            unique_document_ids = list(
                dict.fromkeys(
                    document_id
                    for document_ids in ranked_ids_by_check
                    for document_id in document_ids
                )
            )
            document_load_started_at = perf_counter()
            documents = {
                document["document_id"]: document
                for document in cls._load_documents(
                    connection=connection,
                    document_ids=unique_document_ids,
                )
            }
            document_load_duration = (
                perf_counter() - document_load_started_at
            )
            logger.info(
                "[LEGAL_RETRIEVAL][TIMING] "
                "fts_query=%.3fs document_load=%.3fs total=%.3fs",
                fts_duration,
                document_load_duration,
                perf_counter() - total_started_at,
            )

            return [
                {
                    "contract_text": check["contract_text"],
                    "contexts": [
                        documents[document_id]
                        for document_id in document_ids
                        if document_id in documents
                    ],
                }
                for check, document_ids in zip(
                    legal_checks,
                    ranked_ids_by_check,
                )
            ]
        finally:
            connection.close()

    @classmethod
    def _load_and_validate_fts(
        cls,
        connection,
    ) -> None:

        try:
            connection.execute("LOAD fts")
        except duckdb.Error as exc:
            raise RuntimeError(
                "DuckDB FTS extension is not available. Run "
                "python scripts/setup_legal_fts.py --rebuild first."
            ) from exc

        index_exists = connection.execute(
            """
            SELECT COUNT(*) > 0
            FROM information_schema.schemata
            WHERE schema_name = ?
            """,
            [cls.FTS_SCHEMA],
        ).fetchone()[0]

        if not index_exists:
            raise RuntimeError(
                "Legal FTS index is not initialized. Run "
                "python scripts/setup_legal_fts.py --rebuild first."
            )

    @classmethod
    def _search_document_ids(
        cls,
        connection,
        metadata_seeds: Any,
    ) -> list[str]:

        normalized_seeds = cls._normalize_seeds(
            metadata_seeds
        )

        if not normalized_seeds:
            return []

        search_query = " ".join(
            seed
            for seeds in normalized_seeds.values()
            for seed in seeds
        )
        rows = connection.execute(
            f"""
            SELECT document_id
            FROM (
                SELECT
                    document_id,
                    fts_main_legal_search.match_bm25(
                        document_id,
                        ?
                    ) AS score
                FROM legal_search
            ) AS ranked
            WHERE score IS NOT NULL
            ORDER BY score DESC
            LIMIT {cls.LEGAL_TOP_K}
            """,
            [search_query],
        ).fetchall()

        return [row[0] for row in rows]

    @classmethod
    def _load_documents(
        cls,
        connection,
        document_ids: list[str],
    ) -> list[dict[str, Any]]:

        if not document_ids:
            return []

        placeholders = ", ".join(
            "?" for _ in document_ids
        )

        rows = connection.execute(
            f"""
            SELECT document_id, vn_text, metadata
            FROM legal_documents
            WHERE document_id IN ({placeholders})
            """,
            document_ids,
        ).fetchall()

        documents = {
            document_id: {
                "document_id": document_id,
                "metadata": cls._parse_metadata(metadata),
                "vn_text": vn_text,
            }
            for document_id, vn_text, metadata in rows
        }

        return [
            documents[document_id]
            for document_id in document_ids
            if document_id in documents
        ]

    @classmethod
    def _normalize_seeds(
        cls,
        metadata_seeds: Any,
    ) -> dict[str, list[str]]:

        if not isinstance(metadata_seeds, dict):
            return {}

        normalized = {}

        for field, seeds in metadata_seeds.items():
            if (
                field not in cls.SUPPORTED_METADATA_FIELDS
                or not isinstance(seeds, list)
            ):
                continue

            values = [
                seed.strip()
                for seed in seeds
                if isinstance(seed, str)
                and seed.strip()
            ]

            if values:
                normalized[field] = values

        return normalized

    @staticmethod
    def _parse_metadata(
        raw_metadata: Any,
    ) -> dict[str, Any]:

        if isinstance(raw_metadata, dict):
            return raw_metadata

        if isinstance(raw_metadata, str):
            parsed = json.loads(raw_metadata)

            if isinstance(parsed, dict):
                return parsed

        raise ValueError(
            "Legal document metadata must be a JSON object."
        )
