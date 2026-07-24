from uuid import UUID

from app.enums.prompt_code import (
    PromptCode,
)

from app.repositories.ai_model_repository import (
    AIModelRepository,
)

from app.repositories.ai_prompt_repository import (
    AIPromptRepository,
)

from app.services.llm.azure_openai_service import (
    AzureOpenAIService,
)

from app.services.session_memory.session_memory_service import (
    SessionMemoryService,
)


class RagService:

    def __init__(self):
        self.llm = AzureOpenAIService()

    async def ask(
        self,
        db,
        conversation_id: UUID,
        question: str,
        chunks: list,
        model_id: UUID,
    ):

        # ======================================
        # Conversation Memory
        # ======================================

        history = await (
            SessionMemoryService
            .build_context(
                db=db,
                conversation_id=conversation_id,
            )
        )

        # ======================================
        # Prompt
        # ======================================

        prompt = await (
            AIPromptRepository
            .get_by_code(
                db=db,
                code=PromptCode.RAG_CHAT,
            )
        )

        if prompt is None:
            raise Exception(
                "Prompt RAG_CHAT not found."
            )

        # ======================================
        # AI Model
        # ======================================

        model = await (
            AIModelRepository
            .get_by_id(
                db=db,
                id=model_id,
            )
        )

        if model is None:
            raise Exception(
                "AI Model not found."
            )

        # ======================================
        # Build Context
        # ======================================

        context = "\n\n".join(
            chunk["content"]
            for chunk in chunks
            if chunk.get("content")
        )

        # ======================================
        # Build System Prompt
        # ======================================

        system_prompt = (
            prompt.system_prompt
            .replace(
                "{{history}}",
                history or "",
            )
            .replace(
                "{{context}}",
                context,
            )
        )

        # ======================================
        # Chat Messages
        # ======================================

        messages = [
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": question,
            },
        ]

        # ======================================
        # Generate
        # ======================================

        answer = await self.llm.chat(
            model=model.model_name,
            messages=messages,
            temperature=0.2,
        )

        return answer