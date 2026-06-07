from fastapi import *

from sqlalchemy.ext.asyncio import (
    AsyncSession
)

from app.core.database import (
    get_db
)

from app.repositories.permission_repository import (
    PermissionRepository
)


router = APIRouter(

    prefix=
    "/permissions",

    tags=
    ["Permissions"]

)


@router.get(

"/{role}"

)

async def get_permission(

    role:
    str,

    db:
    AsyncSession

    =

    Depends(
        get_db
    )

):


    result = await (

        PermissionRepository
        .get_role_access(

            db,

            role
        )

    )


    return result