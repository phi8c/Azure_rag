from uuid import UUID

from sqlalchemy import (
    select
)

from sqlalchemy.ext.asyncio import (
    AsyncSession
)

from app.models.recruitment_campaign import (
    RecruitmentCampaign
)


class RecruitmentCampaignRepository:

    @staticmethod
    async def create(
        db: AsyncSession,
        role_id: int,
        title: str,
        job_description: str,
        created_by: UUID | None = None
    ):
        item = RecruitmentCampaign(
            role_id=role_id,
            title=title,
            job_description=job_description,
            created_by=created_by
        )

        db.add(item)

        await db.commit()

        await db.refresh(item)

        return item

    @staticmethod
    async def get_all(
        db: AsyncSession
    ):
        query = await db.execute(
            select(
                RecruitmentCampaign
            )
            .order_by(
                RecruitmentCampaign.created_at.desc()
            )
        )

        return (
            query
            .scalars()
            .all()
        )

    @staticmethod
    async def get_by_id(
        db: AsyncSession,
        id: UUID
    ):
        query = await db.execute(
            select(
                RecruitmentCampaign
            )
            .where(
                RecruitmentCampaign.id == id
            )
        )

        return (
            query
            .scalar_one_or_none()
        )