from azure.search.documents import (
    SearchClient
)

from azure.search.documents.models import (
    VectorizedQuery
)

from azure.core.credentials import (
    AzureKeyCredential
)

from openai import (
    AzureOpenAI
)

from app.core.settings import settings

from app.repositories.rag_config_repository import (
    WorkspaceConfigRepository
)
from app.enums.prompt_code import PromptCode

from app.services.llm.azure_openai_service import AzureOpenAIService
import json


class AzureSearchService:
    
    
    
    
    @staticmethod
    async def analyze_question_to_query(question: str) -> str:

        prompt = f"""
    Bạn là bộ viết lại câu hỏi (query rewriting) cho hệ thống retrieval tài liệu nội bộ.

    Nhiệm vụ: đọc câu hỏi của người dùng và viết lại thành 1 đoạn văn ngắn,
    dùng để tìm kiếm full-text (BM25) trong kho tài liệu, sao cho dễ khớp
    với nội dung chunk tài liệu gốc nhất có thể.

    Yêu cầu:
    - Chỉ trả về đúng 1 đoạn văn bản thuần (plain text), KHÔNG JSON, KHÔNG markdown, không giải thích gì thêm.
    - Giữ nguyên ngôn ngữ của câu hỏi gốc.
    - Có thể mở rộng thêm từ đồng nghĩa / thuật ngữ liên quan nếu giúp tăng khả năng match,
    nhưng không lan man, không thêm ý ngoài phạm vi câu hỏi.

    Câu hỏi: "{question}"

    Đoạn văn tìm kiếm:
    """

        result = await (
            AzureOpenAIService()
            .generate(
                model="gpt-5.1",
                prompt=prompt,
                temperature=0.2,
            )
        )

        print("Rewritten search query:", result)

        search_text_query = result.strip() if result else question

        return search_text_query


   
    @staticmethod
    async def retrieve(question: str, permissions: list):

        client = SearchClient(
            endpoint=settings.AZURE_SEARCH_ENDPOINT,
            index_name=settings.AZURE_SEARCH_INDEX,
            credential=AzureKeyCredential(settings.AZURE_SEARCH_KEY),
        )

        filters = []
        for p in permissions:
            filters.append(
                f"(department eq '{p['department']}' and sensitivity le {p['max_sensitivity']})"
            )
        azure_filter = " or ".join(filters)

        search_text_query = await AzureSearchService.analyze_question_to_query(question)

        openai_client = AzureOpenAI(
            api_key=settings.AZURE_OPENAI_API_KEY,
            azure_endpoint=settings.AZURE_OPENAI_ENDPOINT,
            api_version=settings.AZURE_OPENAI_API_VERSION,
        )

        embedding_response = openai_client.embeddings.create(
            model=settings.AZURE_OPENAI_EMBEDDING_DEPLOYMENT,
            input=question,
        )
        query_embedding = embedding_response.data[0].embedding

        vector_query = VectorizedQuery(
            vector=query_embedding,
            k_nearest_neighbors=10,
            fields="text_vector",
        )

        results = list(client.search(
            search_text=search_text_query,
            vector_queries=[vector_query],
            filter=azure_filter,
            top=10,
        ))

        if not results:
            return []

        top1 = results[0]
        top1_parent_id = top1.get("parent_id")
        top1_title = top1.get("title")

        print("Top1 chunk thuộc document:", top1_title, "| parent_id:", top1_parent_id)

        full_doc_chunks = list(client.search(
            search_text="*",
            filter=f"parent_id eq '{top1_parent_id}'",
            top=1000,
        ))

        return [
        {
            "score": doc.get("@search.score"),
            "chunk_id": doc.get("chunk_id"),
            "parent_id": doc.get("parent_id"),
            "title": doc.get("title"),
            "content": doc.get("chunk"),
            "source_file": doc.get("source_file"),
            "department": doc.get("department"),
            "owner_role": doc.get("owner_role"),
            "security_level": doc.get("security_level"),
            "document_type": doc.get("document_type"),
            "sensitivity": doc.get("sensitivity"),
            "source_url": doc.get("source_url"),
        }
        for doc in full_doc_chunks
    ]
    @staticmethod
    def retrieve_helpdesk(
        question: str,
        top_k: int,
    ):

        client = SearchClient(

            endpoint=
            settings
            .AZURE_SEARCH_ENDPOINT,

            index_name=
            settings
            .AZURE_SEARCH_INDEX,

            credential=
            AzureKeyCredential(

                settings
                .AZURE_SEARCH_KEY

            )

        )

        openai_client = AzureOpenAI(

            api_key=
            settings
            .AZURE_OPENAI_API_KEY,

            azure_endpoint=
            settings
            .AZURE_OPENAI_ENDPOINT,

            api_version=
            settings
            .AZURE_OPENAI_API_VERSION,

        )

        embedding_response = (

            openai_client
            .embeddings
            .create(

                model=
                settings
                .AZURE_OPENAI_EMBEDDING_DEPLOYMENT,

                input=
                question,

            )

        )

        query_embedding = (

            embedding_response
            .data[0]
            .embedding

        )

        vector_query = (

            VectorizedQuery(

                vector=
                query_embedding,

                k_nearest_neighbors=
                top_k,

                fields=
                "text_vector",

            )

        )

        azure_filter = (
            "workspace eq 'HELPDESK'"
        )

        print(
            "Azure Filter:",
            azure_filter,
        )

        results = client.search(

            search_text=
            question,

            vector_queries=[
                vector_query,
            ],

            filter=
            azure_filter,

            top=
            20,

        )

        return [

            {

                "score":
                doc.get("@search.score"),

                "chunk_id":
                doc.get("chunk_id"),

                "parent_id":
                doc.get("parent_id"),

                "title":
                doc.get("title"),

                "content":
                doc.get("chunk"),

                "source_file":
                doc.get("source_file"),

                "department":
                doc.get("department"),

                "owner_role":
                doc.get("owner_role"),

                "security_level":
                doc.get("security_level"),

                "document_type":
                doc.get("document_type"),

                "sensitivity":
                doc.get("sensitivity"),
                "source_url":
                doc.get("source_url"),

            }

            for doc in results

        ]
            
            
            
            