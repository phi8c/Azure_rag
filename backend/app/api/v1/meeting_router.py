from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)

from sqlalchemy.ext.asyncio import (
    AsyncSession,
)

from app.core.database import (
    get_db,
)

from app.services.meeting.meeting_service import (
    MeetingService,
)


router = APIRouter(
    prefix="/meeting",
    tags=["Meeting"],
)


@router.get("")
async def get_meetings(
    db: AsyncSession = Depends(
        get_db
    ),
):

    return await (
        MeetingService
        .get_all(
            db=db,
        )
    )


@router.get("/{id}")
async def get_meeting(
    id: UUID,
    db: AsyncSession = Depends(
        get_db
    ),
):

    result = await (
        MeetingService
        .get_by_id(
            db=db,
            id=id,
        )
    )

    if result is None:

        raise HTTPException(
            status_code=404,
            detail="Meeting not found.",
        )

    return result