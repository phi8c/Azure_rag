from dataclasses import dataclass

from uuid import UUID

from fastapi import UploadFile


@dataclass(slots=True)
class CreateReviewRequest:

    model_id: UUID
    
    
    job_description: str

    files: list[UploadFile]