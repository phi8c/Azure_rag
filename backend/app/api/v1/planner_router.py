from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import (
    get_db,
)

from app.api.dependencies.auth import (
    get_current_user,
)

from app.models.user_model import User

from app.services.microsoft.planner_service import (
    PlannerService,
)

router = APIRouter(
    prefix="/planner",
    tags=["Planner"],
)


@router.get("/tasks")
async def get_tasks(
    current_user: User = Depends(
        get_current_user,
    ),
    db: AsyncSession = Depends(
        get_db,
    ),
):

    return await PlannerService.get_my_tasks(
        db=db,
        user_id=str(current_user.id),
    )