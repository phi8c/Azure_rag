from sqlalchemy import (
    select
)

from sqlalchemy.ext.asyncio import (
    AsyncSession
)


from app.models.ai_prompt import (
    AIPrompt
)
from uuid import UUID

from app.enums.prompt_code import PromptCode


class AIPromptRepository:

    @staticmethod
    async def get_by_code(
        db: AsyncSession,
        code: PromptCode,
    ):
        query = await db.execute(
            select(AIPrompt).where(
                AIPrompt.code == code.value,
                AIPrompt.is_active == True,
            )
        )

        return query.scalar_one_or_none()
        
    @staticmethod
    async def get_by_id(
        db: AsyncSession,
        id: UUID,
    ):
        query = await db.execute(
            select(
                AIPrompt
            )
            .where(
                AIPrompt.id == id,
                AIPrompt.is_active == True,
            )
        )

        return (
            query
            .scalar_one_or_none()
        )
        
        
 