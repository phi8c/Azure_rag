from uuid import UUID

from pydantic import BaseModel


class RecruitmentCampaignChatRequest(
    BaseModel
):

    campaign_id: UUID

    model_id: UUID

    question: str