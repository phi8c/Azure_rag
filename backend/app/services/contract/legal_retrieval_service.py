import json
import math
import re
import unicodedata
from collections import Counter
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

    _CITATION_FIELDS = {
        "raw",
        "target",
        "dieu",
        "khoan",
        "diem",
    }

    _TOKEN_RE = re.compile(r"[^\W_]+", re.UNICODE)

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
            started_at = perf_counter()
            candidates = cls._load_candidates(
                connection
            )
            logger.info(
                "[CONTRACT_ADVANCED] legal_candidate_load "
                "completed in %.3fs candidates=%d",
                perf_counter() - started_at,
                len(candidates),
            )

            indexes = cls._build_indexes(
                candidates
            )
            ranked_ids_by_check = []

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
                document_ids = cls._rank_document_ids(
                    candidates=candidates,
                    indexes=indexes,
                    metadata_seeds=check.get(
                        "metadata_seeds",
                        {},
                    ),
                )
                logger.info(
                    "[CONTRACT_ADVANCED] legal_retrieval completed "
                    "check=%d/%d in %.3fs result_count=%d",
                    check_index,
                    len(legal_checks),
                    perf_counter() - started_at,
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
            documents = {
                document["document_id"]: document
                for document in cls._load_documents(
                    connection=connection,
                    document_ids=unique_document_ids,
                )
            }

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
    def _load_candidates(
        cls,
        connection,
    ) -> list[dict[str, Any]]:

        rows = connection.execute(
            """
            SELECT document_id, metadata
            FROM legal_documents
            """
        ).fetchall()

        candidates = []

        for document_id, raw_metadata in rows:
            metadata = cls._parse_metadata(
                raw_metadata
            )

            candidates.append(
                {
                    "document_id": document_id,
                    "metadata": metadata,
                    "field_tokens": {
                        field: cls._tokenize(
                            cls._metadata_value_to_text(
                                field,
                                metadata.get(field),
                            )
                        )
                        for field in cls.SUPPORTED_METADATA_FIELDS
                    },
                }
            )

        return candidates

    @classmethod
    def _build_indexes(
        cls,
        candidates: list[dict[str, Any]],
    ) -> dict[str, dict[str, Any]]:

        field_indexes = {
            field: cls._build_bm25_index(
                [
                    candidate["field_tokens"][field]
                    for candidate in candidates
                ]
            )
            for field in cls.SUPPORTED_METADATA_FIELDS
        }
        global_documents = [
            [
                token
                for tokens in candidate["field_tokens"].values()
                for token in tokens
            ]
            for candidate in candidates
        ]
        field_indexes["__global__"] = (
            cls._build_bm25_index(
                global_documents
            )
        )

        return field_indexes

    @classmethod
    def _rank_document_ids(
        cls,
        candidates: list[dict[str, Any]],
        indexes: dict[str, dict[str, Any]],
        metadata_seeds: Any,
    ) -> list[str]:

        normalized_seeds = cls._normalize_seeds(
            metadata_seeds
        )

        if not normalized_seeds or not candidates:
            return []

        scores = [0.0] * len(candidates)

        for field, seeds in normalized_seeds.items():
            query_tokens = cls._tokenize(
                " ".join(seeds)
            )

            field_scores = cls._bm25_scores(
                index=indexes[field],
                query_tokens=query_tokens,
            )

            fallback_scores = cls._bm25_scores(
                index=indexes["__global__"],
                query_tokens=query_tokens,
            )

            for index in range(len(candidates)):
                scores[index] += (
                    field_scores[index]
                    + fallback_scores[index] * 0.2
                )

        ranked_indexes = sorted(
            (
                index
                for index, score in enumerate(scores)
                if score > 0
            ),
            key=lambda index: scores[index],
            reverse=True,
        )[:cls.LEGAL_TOP_K]

        return [
            candidates[index]["document_id"]
            for index in ranked_indexes
        ]

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

    @classmethod
    def _metadata_value_to_text(
        cls,
        field: str,
        value: Any,
    ) -> str:

        if value is None:
            return ""

        if field == "citations":
            return cls._citation_value_to_text(value)

        if isinstance(value, dict):
            return " ".join(
                cls._metadata_value_to_text(
                    field,
                    item,
                )
                for item in value.values()
            )

        if isinstance(value, list):
            return " ".join(
                cls._metadata_value_to_text(
                    field,
                    item,
                )
                for item in value
            )

        if isinstance(value, (str, int, float)):
            return str(value)

        return ""

    @classmethod
    def _citation_value_to_text(
        cls,
        value: Any,
    ) -> str:

        if isinstance(value, list):
            return " ".join(
                cls._citation_value_to_text(item)
                for item in value
            )

        if isinstance(value, dict):
            return " ".join(
                str(value[field])
                for field in cls._CITATION_FIELDS
                if value.get(field) is not None
            )

        if isinstance(value, str):
            return value

        return ""

    @classmethod
    def _tokenize(
        cls,
        value: str,
    ) -> list[str]:

        normalized = unicodedata.normalize(
            "NFKC",
            value,
        ).casefold()

        return cls._TOKEN_RE.findall(
            normalized
        )

    @staticmethod
    def _build_bm25_index(
        documents: list[list[str]],
    ) -> dict[str, Any]:

        frequencies = [
            Counter(document)
            for document in documents
        ]
        document_frequencies = Counter()

        for frequency in frequencies:
            document_frequencies.update(
                frequency.keys()
            )

        return {
            "documents": documents,
            "frequencies": frequencies,
            "document_frequencies": document_frequencies,
            "document_count": len(documents),
            "average_length": (
                sum(len(document) for document in documents)
                / len(documents)
                if documents
                else 0.0
            ),
        }

    @staticmethod
    def _bm25_scores(
        index: dict[str, Any],
        query_tokens: list[str],
        k1: float = 1.5,
        b: float = 0.75,
    ) -> list[float]:

        documents = index["documents"]
        document_count = index["document_count"]
        average_length = index["average_length"]

        if (
            not documents
            or not query_tokens
            or average_length == 0
        ):
            return [0.0] * document_count

        frequencies = index["frequencies"]
        query_terms = set(query_tokens)
        document_frequencies = index[
            "document_frequencies"
        ]

        scores = []

        for document, frequency in zip(
            documents,
            frequencies,
        ):
            score = 0.0

            for term in query_terms:
                term_frequency = frequency.get(term, 0)

                if term_frequency == 0:
                    continue

                document_frequency = document_frequencies[term]
                inverse_document_frequency = math.log(
                    1
                    + (
                        document_count
                        - document_frequency
                        + 0.5
                    )
                    / (document_frequency + 0.5)
                )
                denominator = (
                    term_frequency
                    + k1
                    * (
                        1
                        - b
                        + b
                        * len(document)
                        / average_length
                    )
                )

                score += (
                    inverse_document_frequency
                    * term_frequency
                    * (k1 + 1)
                    / denominator
                )

            scores.append(score)

        return scores
