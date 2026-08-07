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

from app.enums.prompt_code import ( PromptCode)
from app.repositories.rag_config_repository import WorkspaceConfigRepository


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
        mode: PromptCode,
        workspace_code: str,
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

        # ======================================
        # Prompt
        # ======================================

        if mode == PromptCode.PUBLIC:

            prompt = await AIPromptRepository.get_by_code(
                db=db,
                code=mode,
            )

        elif mode == PromptCode.INTERNAL:

            prompt = await AIPromptRepository.get_by_code(
                db=db,
                code=mode,
            )

        elif mode == PromptCode.COMBINE:

            prompt = await AIPromptRepository.get_by_code(
                db=db,
                code=mode,
            )

        else:

            raise Exception("Invalid chat mode.")

        if prompt is None:
            raise Exception("Prompt not found.")


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

        contexts = []

        for chunk in chunks:

            contexts.append(
                chunk["content"]
            )

        context = "\n\n".join(contexts)

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
        
        
        model_config = await (
        WorkspaceConfigRepository
        .get_model_config_by_workspace_code(

            db=db,

            workspace_code=
            workspace_code,

        )
    ) 
        temperature = float(
                model_config.temperature
            )
        
        max_tokens = int(
                model_config.max_tokens
            )
        
        

        answer = await self.llm.chat(
            model=model.model_name,
            messages=messages,
            temperature=temperature,
            max_completion_tokens=max_tokens
        )

        return answer