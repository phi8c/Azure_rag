from sqlalchemy.ext.asyncio import AsyncSession

from app.core.not_found_exception import (
    NotFoundException,
)

from app.enums.review_job_status import (
    ReviewJobStatus,
)
from app.enums.review_queue import (
    ReviewQueue,
)
from app.enums.review_task_status import (
    ReviewTaskStatus,
)

from app.schemas.create_review_request import (
    CreateReviewRequest,
)
from app.models.review_job import (
    ReviewJob,
)
from app.models.review_task import (
    ReviewTask,
)

from app.repositories.ai_model_repository import (
    AIModelRepository,
)
from app.repositories.review_job_repository import (
    ReviewJobRepository,
)
from app.repositories.review_task_repository import (
    ReviewTaskRepository,
)

from app.services.temp.temp_file_service import (
    TempFileService,
)

from app.shared.queue.local_queue_provider import (
    queue_provider,
)
from app.utils.queue.queue_message import (
    QueueMessage,
)

from app.review.messages.review_task_message import (
    ReviewTaskMessage,
)

from uuid import UUID





from app.core.not_found_exception import (
    NotFoundException,
)
from app.enums.review_job_status import (
    ReviewJobStatus,
)
from app.repositories.review_job_repository import (
    ReviewJobRepository,
)
from app.repositories.review_task_repository import (
    ReviewTaskRepository,
)
from app.schemas.review_dto import (
    ReviewJobResultResponse,
    ReviewTaskResultResponse,
)


class ReviewService:

    @staticmethod
    async def create_review(
        db: AsyncSession,
        request: CreateReviewRequest,
        created_by=None,
    ) -> ReviewJob:

        model = await AIModelRepository.get_by_id(
            db=db,
            id=request.model_id,
        )

        if model is None:
            raise NotFoundException(
                "AI Model not found.",
            )

        review_job = ReviewJob(
            model_id=model.id,
            job_description=request.job_description,
            status=ReviewJobStatus.QUEUED,
            total_files=len(
                request.files,
            ),
            created_by=created_by,
        )

        await ReviewJobRepository.create(
            db=db,
            review_job=review_job,
        )

        await db.flush()

        review_tasks: list[ReviewTask] = []

        try:

            for file in request.files:

                temp_file = await TempFileService.save(
                    job_id=review_job.id,
                    file=file,
                )


                review_task = ReviewTask(
                    job_id=review_job.id,
                    status=ReviewTaskStatus.QUEUED,
                    file_name=file.filename,
                    file_path=temp_file.file_path,
                    file_size=temp_file.file_size,
                    mime_type=file.content_type or "",
                )

                await ReviewTaskRepository.create(
                    db=db,
                    review_task=review_task,
                )

                review_tasks.append(
                    review_task,
                )

            await db.commit()

        except Exception:

            await db.rollback()

            TempFileService.delete_job_directory(
                review_job.id,
            )

            raise

        for review_task in review_tasks:

            await queue_provider.publish(
                QueueMessage(
                    queue_name=ReviewQueue.REVIEW,
                    payload=ReviewTaskMessage(
                        task_id=review_task.id,
                    ),
                )
            )

        return review_job
    
    @staticmethod
    async def get_result(
    db: AsyncSession,
    job_id: UUID,
) -> ReviewJobResultResponse:

        job = await ReviewJobRepository.get_by_id(
            db=db,
            id=job_id,
        )

        if job is None:

            raise NotFoundException(
                "Review job not found.",
            )

        tasks = await (
            ReviewTaskRepository.get_by_job_id(
                db=db,
                job_id=job_id,
            )
        )

        completed_files = sum(
            task.status == ReviewTaskStatus.COMPLETED
            for task in tasks
        )

        failed_files = sum(
            task.status == ReviewTaskStatus.FAILED
            for task in tasks
        )

        return ReviewJobResultResponse(
            job_id=job.id,
            status=job.status,
            total_files=job.total_files,
            completed_files=completed_files,
            failed_files=failed_files,
            tasks=[
                ReviewTaskResultResponse(
                    task_id=task.id,
                    file_name=task.file_name,
                    status=task.status,
                    review_result=task.review_result,
                )
                for task in tasks
            ],
        )