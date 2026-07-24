from uuid import UUID

from sqlalchemy.ext.asyncio import (
    AsyncSession
)

from app.repositories.recruitment_campaign_repository import (
    RecruitmentCampaignRepository
)


class RecruitmentService:

    @staticmethod
    async def create_campaign(
        db: AsyncSession,
        role_id: int,
        title: str,
        job_description: str,
        created_by: UUID | None = None
    ):
        return await (
            RecruitmentCampaignRepository.create(
                db=db,
                role_id=role_id,
                title=title,
                job_description=job_description,
                created_by=created_by
            )
        )