import asyncio
import gzip
import json
import logging
import re
import unicodedata
from typing import Any

from azure.core.credentials import AzureKeyCredential
from azure.search.documents.aio import SearchClient
from azure.storage.blob.aio import BlobServiceClient

from app.core.settings import settings


log = logging.getLogger("legal_search")


class LegalSearchService:
    """
    Tra cứu văn bản pháp luật:
      1. Seed -> tìm trên Azure AI Search (BM25, chỉ metadata) lấy top văn bản.
      2. Mỗi văn bản -> tải toàn văn từ Azure Blob (legal-vbpl/{id}.json.gz).
      3. Chọn các Điều liên quan nhất trong giới hạn ký tự.

    Trả về cấu trúc {document_id, metadata, vn_text}.
    """

    TOP_K = 4
    MAX_CHARS_PER_DOCUMENT = 12000

    # Seed field trong analyzer -> field trong index legal-vbpl
    SEED_FIELD_MAP = {
        "doc_number": "doc_number",
        "title": "title",
        "doc_type": "doc_type",
        "legal_area": "legal_area",
        "issuing_body": "issuing_body",
        "issuer": "issuer",
        "article_titles": "article_titles",
        "parent_acts": "parent_acts",
        "citations": "citation_targets",
    }

    RESULT_FIELDS = [
        "id",
        "doc_number",
        "title",
        "doc_type",
        "legal_area",
        "issuing_body",
        "issuer",
        "article_titles",
        "parent_acts",
        "tier",
        "section",
        "year",
        "status",
        "issue_date",
        "effective_date",
        "signer",
        "url",
        "num_articles",
    ]

    _search_client: SearchClient | None = None
    _blob_service: BlobServiceClient | None = None

    @classmethod
    def _get_search_client(cls) -> SearchClient:
        if cls._search_client is None:
            cls._search_client = SearchClient(
                endpoint=settings.AZURE_SEARCH_ENDPOINT,
                index_name=settings.AZURE_LEGAL_SEARCH_INDEX,
                credential=AzureKeyCredential(settings.AZURE_SEARCH_KEY),
            )
        return cls._search_client

    @classmethod
    def _get_blob_service(cls) -> BlobServiceClient:
        if cls._blob_service is None:
            credential = (
                (settings.AZURE_STORAGE_SAS_TOKEN or "").lstrip("?")
                or settings.AZURE_STORAGE_KEY
            )
            cls._blob_service = BlobServiceClient(
                account_url=settings.AZURE_STORAGE_ACCOUNT_URL,
                credential=credential,
            )
        return cls._blob_service

    # ------------------------------------------------------------------
    # Truy vấn
    # ------------------------------------------------------------------

    @staticmethod
    def _escape_phrase(value: str) -> str:
        return value.replace("\\", "\\\\").replace('"', '\\"')

    # Từ không mang nghĩa để tìm kiếm, bỏ khi tạo truy vấn theo từ
    STOPWORDS = {
        "và", "của", "theo", "cho", "các", "một", "có", "là", "được",
        "trong", "với", "về", "để", "này", "đó", "khi", "từ", "tại",
    }

    @classmethod
    def _words(cls, seed: str) -> list[str]:
        words = [
            word
            for word in re.findall(r"\w+", seed.lower())
            if len(word) > 1 and word not in cls.STOPWORDS
        ]
        return words

    @classmethod
    def _field_clauses(cls, metadata_seeds: dict[str, list[str]], joiner: str) -> str:
        clauses = []

        for field, seeds in metadata_seeds.items():
            index_field = cls.SEED_FIELD_MAP.get(field)

            if not index_field:
                continue

            for seed in seeds:
                words = cls._words(seed)

                if not words:
                    continue

                body = f" {joiner} ".join(cls._escape_term(w) for w in words)
                clauses.append(f"{index_field}:({body})")

        return " OR ".join(clauses)

    @staticmethod
    def _escape_term(value: str) -> str:
        return re.sub(r'([+\-&|!(){}\[\]^"~*?:\/])', r"\", value)

    @classmethod
    def build_search_query(cls, metadata_seeds: dict[str, list[str]]) -> str:
        """Truy vấn AND: văn bản phải chứa đủ các từ của seed trong field tương ứng."""
        return cls._field_clauses(metadata_seeds, "AND")

    @classmethod
    def build_fallback_query(cls, metadata_seeds: dict[str, list[str]]) -> str:
        """Truy vấn OR: dùng khi truy vấn AND không có kết quả nào."""
        return cls._field_clauses(metadata_seeds, "OR")

    @staticmethod
    def _all_seed_text(metadata_seeds: dict[str, list[str]]) -> str:
        return " ".join(
            seed
            for seeds in metadata_seeds.values()
            for seed in seeds
        )

    @classmethod
    async def _run_query(cls, query: str) -> list[dict[str, Any]]:
        results = await cls._get_search_client().search(
            search_text=query,
            query_type="full",
            top=cls.TOP_K,
            select=cls.RESULT_FIELDS,
        )
        return [doc async for doc in results]

    @classmethod
    async def _search(cls, metadata_seeds: dict[str, list[str]]) -> list[dict[str, Any]]:
        query = cls.build_search_query(metadata_seeds)

        if query:
            hits = await cls._run_query(query)

            if hits:
                return hits

            fallback = cls.build_fallback_query(metadata_seeds)

            if fallback:
                return await cls._run_query(fallback)

            return []

        # Không có seed nào map được sang field -> tìm toàn bộ trên các field searchable
        text = cls._all_seed_text(metadata_seeds).strip()

        if not text:
            raise ValueError("Legal search query must not be empty.")

        results = await cls._get_search_client().search(
            search_text=text,
            query_type="simple",
            top=cls.TOP_K,
            select=cls.RESULT_FIELDS,
        )
        return [doc async for doc in results]

    # ------------------------------------------------------------------
    # Tải và chọn nội dung
    # ------------------------------------------------------------------

    @classmethod
    async def _load_blob(cls, doc_id: str) -> dict[str, Any] | None:
        client = cls._get_blob_service().get_blob_client(
            container=settings.AZURE_LEGAL_BLOB_CONTAINER,
            blob=f"{doc_id}.json.gz",
        )

        try:
            stream = await client.download_blob()
            raw = await stream.readall()
        except Exception as exc:
            log.warning("không tải được blob %s: %s", doc_id, exc)
            return None

        return json.loads(gzip.decompress(raw).decode("utf-8"))

    @staticmethod
    def _tokens(text: str) -> set[str]:
        folded = unicodedata.normalize("NFD", text.lower().replace("đ", "d"))
        folded = "".join(ch for ch in folded if unicodedata.category(ch) != "Mn")
        return set(re.findall(r"[a-z0-9]{3,}", folded))

    @classmethod
    def select_text(cls, blob: dict[str, Any], query_text: str) -> str:
        """Chọn các Điều có nhiều từ trùng với câu hỏi nhất, trong giới hạn ký tự."""
        max_chars = cls.MAX_CHARS_PER_DOCUMENT
        vn_text = blob.get("vn_text") or ""
        articles = blob.get("articles") or []

        if not articles:
            # Văn bản không tách được Điều -> lấy phần đầu toàn văn
            return vn_text[:max_chars]

        terms = cls._tokens(query_text)
        scored = []

        for idx, article in enumerate(articles):
            preview = f"{article.get('title', '')} {article.get('text', '')[:2000]}"
            overlap = len(terms & cls._tokens(preview))
            scored.append((overlap, idx))

        scored.sort(key=lambda item: (-item[0], item[1]))

        chosen: list[int] = []
        total = 0

        for _, idx in scored:
            text = articles[idx].get("text", "")

            if total + len(text) > max_chars:
                if chosen:
                    continue
                text = text[:max_chars]

            chosen.append(idx)
            total += len(text)

        chosen.sort()

        return "\n\n".join(articles[idx].get("text", "") for idx in chosen)

    # ------------------------------------------------------------------
    # API
    # ------------------------------------------------------------------

    @classmethod
    async def retrieve(
        cls,
        metadata_seeds: dict[str, list[str]],
        contract_text: str = "",
    ) -> list[dict[str, Any]]:
        hits = await cls._search(metadata_seeds)

        if not hits:
            return []

        blobs = await asyncio.gather(
            *(cls._load_blob(hit["id"]) for hit in hits)
        )

        query_text = f"{contract_text} {cls._all_seed_text(metadata_seeds)}"
        documents = []

        for hit, blob in zip(hits, blobs):
            if blob is None:
                continue

            documents.append({
                "document_id": hit["id"],
                "metadata": {
                    key: hit.get(key)
                    for key in cls.RESULT_FIELDS
                    if key != "id" and hit.get(key) is not None
                },
                "vn_text": cls.select_text(blob, query_text),
            })

        return documents
