from uuid import UUID
from datetime import datetime

from pydantic import BaseModel


class RecruitmentCampaignCreate(BaseModel):

    role_id: int

    title: str

    job_description: str


class RecruitmentCampaignResponse(BaseModel):

    id: UUID

    role_id: int

    title: str

    job_description: str

    status: str

    created_at: datetime

    class Config:

        from_attributes = True