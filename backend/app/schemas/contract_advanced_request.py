from uuid import UUID

from pydantic import BaseModel, Field


class ContractLegalCheck(BaseModel):
    contract_text: str = Field(min_length=1)
    metadata_seeds: dict[str, list[str]]


class ContractLegalReviewRequest(BaseModel):
    model_id: UUID
    legal_checks: list[ContractLegalCheck]
