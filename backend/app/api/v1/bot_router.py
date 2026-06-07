from fastapi import (
    APIRouter,

    Depends
)

from sqlalchemy.ext.asyncio import (
    AsyncSession
)

from app.core.database import (
    get_db
)

from app.repositories.permission_repository import (
    PermissionRepository
)

from app.services.azure.azure_search_service import (
    AzureSearchService
)

from app.services.rag.rag_service import (
    RagService
)
import json 


router = APIRouter(

    prefix="/bot",

    tags=["Bot"]
)


@router.post(

    "/messages"

)

async def receive_message(

    body:dict,


    db:
    AsyncSession

    =

    Depends(
        get_db
    )

):
    # print(body)


    question = (

        body.get(
            "text",

            ""
        )
        
        
        

    )
    print(
    json.dumps(
        body,
        indent=2
    )
)


    role = (

        "HR_MANAGER"

    )


    permissions = await (

        PermissionRepository

        .get_role_access(

            db,

            role

        )

    )


    chunks = (

        AzureSearchService

        .retrieve(

            question=

            question,


            permissions=

            permissions

        )

    )


    answer = await (

        RagService()

        .ask(

            question=

            question,


            chunks=

            chunks

        )

    )


    return {

        "answer":

        answer
    }