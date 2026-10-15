from uuid import UUID
from typing import AsyncIterator

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

from app.repositories.rag_config_repository import WorkspaceConfigRepository


CHAT_MODES = (
    PromptCode.PUBLIC,
    PromptCode.INTERNAL,
    PromptCode.COMBINE,
)

#
# Dùng chung 1 Azure OpenAI client (connection pool) cho mọi request
#

_shared_llm: AzureOpenAIService | None = None


def _get_shared_llm() -> AzureOpenAIService:

    global _shared_llm

    if _shared_llm is None:

        _shared_llm = AzureOpenAIService()

    return _shared_llm


class RagService:

    def __init__(self):

        self.llm = _get_shared_llm()

    async def ask(
        self,
        db,
        conversation_id: UUID,
        question: str,
        chunks: list,
        model_id: UUID,
        mode: PromptCode,
        workspace_code: str,
    ):

        #
        # Teams bot vẫn dùng history hội thoại
        #

        history = await (
            SessionMemoryService
            .build_context(
                db=db,
                conversation_id=conversation_id,
            )
        )

        chat_config = await self.load_chat_config(
            db=db,
            model_id=model_id,
            mode=mode,
            workspace_code=workspace_code,
        )

        answer = await self.llm.chat(
            model=chat_config["model"],
            messages=self.build_messages(
                chat_config=chat_config,
                question=question,
                chunks=chunks,
                history=history,
            ),
            temperature=chat_config["temperature"],
            max_completion_tokens=chat_config["max_tokens"],
        )

        return answer

    async def ask_stream(
        self,
        chat_config: dict,
        question: str,
        chunks: list,
    ) -> AsyncIterator[str]:

        async for token in self.llm.chat_stream(
            model=chat_config["model"],
            messages=self.build_messages(
                chat_config=chat_config,
                question=question,
                chunks=chunks,
            ),
            temperature=chat_config["temperature"],
            max_completion_tokens=chat_config["max_tokens"],
        ):

            yield token

    async def load_chat_config(
        self,
        db,
        model_id: UUID,
        mode: PromptCode,
        workspace_code: str,
    ) -> dict:

        if mode not in CHAT_MODES:

            raise ValueError("Invalid chat mode.")

        prompt = await AIPromptRepository.get_by_code(
            db=db,
            code=mode,
        )

        if prompt is None:

            raise LookupError("Prompt not found.")

        model = await (
            AIModelRepository
            .get_by_id(
                db=db,
                id=model_id,
            )
        )

        if model is None:

            raise LookupError(
                "AI Model not found."
            )

        model_config = await (
            WorkspaceConfigRepository
            .get_model_config_by_workspace_code(
                db=db,
                workspace_code=workspace_code,
            )
        )

        if model_config is None:

            raise LookupError(
                "Model config not found."
            )

        return {
            "model": model.model_name,
            "system_prompt": prompt.system_prompt,
            "temperature": float(
                model_config.temperature
            ),
            "max_tokens": int(
                model_config.max_tokens
            ),
        }

    @staticmethod
    def build_messages(
        chat_config: dict,
        question: str,
        chunks: list,
        history: str = "",
    ) -> list[dict]:

        context = "\n\n".join(
            chunk["content"]
            for chunk in chunks
            if chunk.get("content")
        )

        system_prompt = (
            chat_config["system_prompt"]
            .replace(
                "{{history}}",
                history or "",
            )
            .replace(
                "{{context}}",
                context,
            )
            .replace(
                "{{question}}",
                question,
            )
        )

        return [
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": question,
            },
        ]
