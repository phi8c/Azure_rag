from uuid import UUID

from pydantic import BaseModel


class ReviewTaskResultResponse(BaseModel):

    task_id: UUID

    file_name: str

    status: str

    review_result: dict | None


class ReviewJobResultResponse(BaseModel):

    job_id: UUID

    status: str

    total_files: int

    completed_files: int

    failed_files: int

    tasks: list[ReviewTaskResultResponse]