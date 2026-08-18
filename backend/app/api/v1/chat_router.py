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

from uuid import uuid4

from app.schemas.chat_schema import (

    ChatRequest,

    ChatResponse

)

from app.repositories.permission_repository import (

    PermissionRepository

)
from app.repositories.role_repository import (
    RoleRepository
)

from app.services.azure.azure_search_service import (

    AzureSearchService

)

from app.services.rag.rag_service import (
    RagService
)

from app.core.not_found_exception import (
    NotFoundException,
)

from app.services.message.message_service import (

 MessageService

)

from app.services.session_memory.session_memory_service import (

 SessionMemoryService

)
from app.services.session_memory.conversation_summary_service import (
    ConversationSummaryService
)

from app.services.rewrite_service.query_rewrite_service import (
    QueryRewriteService
)
from app.services.conversation.conversation_service import (
    ConversationService
)

from app.repositories.conversation_repository import (
    ConversationRepository
)
from app.enums.prompt_code import ( PromptCode
)

import json

from app.repositories.rag_config_repository import WorkspaceConfigRepository

router = APIRouter(

    prefix=
    "/chat",

    tags=
    ["Chat"]

)


from app.services.message.message_service import (

 MessageService

)


@router.post(

 "/query"

)

async def query(

 body:ChatRequest,

 db:AsyncSession

 =

 Depends(

  get_db

 )

):


 role_name = await (
    RoleRepository.get_by_id(
        db=db,
        role_id=body.role_id,
    )
)

 if role_name is None:
    raise NotFoundException(
        "Role not found."
    )
    
 if body.conversation_id is None:
    body.conversation_id = uuid4()

 conversation = await ConversationRepository.get_by_id(
        db=db,
        conversation_id=body.conversation_id,
    )

 if conversation is None:
    await ConversationService.create(
        db=db,
        conversation_id=body.conversation_id,
        title=body.question,
        email=None,
    )

 permissions = await (
    PermissionRepository
    .get_role_access(
        db=db,
        role_name=role_name,
    )
)
#  retrieval_query = await (
#      SessionMemoryService
#      .build_retrieval_query(
#          db=db,
#          conversation_id=body.conversation_id,
#          question = body.question
#      )
#  )



 history = await (
        SessionMemoryService
        .build_context(
            db=db,
            conversation_id=body.conversation_id
        )
    )
 retrieval_query = await (
    QueryRewriteService
    .rewrite(
        history=history,
        question=body.question
    )
)
 print(
    "rewritten query =",
    retrieval_query
)
 
#  print("in ra retrieval", retrieval_query)
 print("in ra permission", permissions)
 
 
 
 chunks = []
 if body.mode != PromptCode.PUBLIC:

    chunks = AzureSearchService.retrieve(
        question=body.question,
        permissions=permissions,
    )



 


 # =======

 # SAVE USER

 # =======

 await (

  MessageService

  .create(

   db,

   {

    "conversation_id":

    body.conversation_id,

    "role":

    "user",

    "content":

    body.question

   }

  )

 )


 rag_service = (

  RagService()

 )
 
 workscpace_code = PromptCode.CHAT_RAG.value


 answer = await (

  rag_service.ask(
    
   db=db,
   conversation_id=body.conversation_id,

   question=

   body.question,

   chunks=

   chunks,
    model_id=body.model_id,
    
    mode=body.mode,
    
    workspace_code=workscpace_code,

  )

 )
 
 if body.mode == PromptCode.PUBLIC:

    result = json.loads(answer)

    answer = result["answer"]

    sources = result["sources"]

 else:

    source_map = {}

    for chunk in chunks:

        file = chunk["source_file"]

        if file not in source_map:

            source_map[file] = {

                "source_file": file,
                
                
                "source_url": chunk["source_url"],

                "excerpt": chunk["content"],

                "type": "internal"

            }

    sources = list(source_map.values())

 # =============

 # SAVE ASSISTANT

 # =============

 await (

  MessageService

  .create(

   db,

   {

    "conversation_id":

    body.conversation_id,

    "role":

    "assistant",

    "content":

    answer

   }

  )

 )
 
#  await (
#     ConversationSummaryService
#     .update_summary(
#         db=db,
#         conversation_id=body.conversation_id
#     )
# )


 return {
    "conversation_id": str(body.conversation_id),
    "title": str(body.question),
    "answer": answer,
    "sources": sources,
    
}
 
 
@router.post("/helpdesk")
async def helpdesk_query(

    body: ChatRequest,

    db: AsyncSession = Depends(
        get_db,
    ),

):

    role_name = await (
        RoleRepository.get_by_id(
            db=db,
            role_id=body.role_id,
        )
    )

    if role_name is None:

        raise NotFoundException(
            "Role not found."
        )

    if body.conversation_id is None:

        body.conversation_id = uuid4()

    conversation = await (
        ConversationRepository.get_by_id(
            db=db,
            conversation_id=body.conversation_id,
        )
    )

    if conversation is None:

        await ConversationService.create(
            db=db,
            conversation_id=body.conversation_id,
            title=body.question,
            email=None,
        )

    history = await (
        SessionMemoryService
        .build_context(
            db=db,
            conversation_id=body.conversation_id,
        )
    )

    retrieval_query = await (
        QueryRewriteService
        .rewrite(
            history=history,
            question=body.question,
        )
    )

    print(
        "rewritten query =",
        retrieval_query,
    )

    # ======================================
    # HELPDESK RETRIEVAL
    # ======================================
    
    top_k = await (
    WorkspaceConfigRepository
    .get_top_k_by_workspace_code(

        db=db,

        workspace_code=
        PromptCode.HELPDESK.value,

    )
)

    chunks = []

    if body.mode != PromptCode.PUBLIC:

        chunks = AzureSearchService.retrieve_helpdesk(
            question=retrieval_query,
            top_k=top_k,
        )

    # ======================================
    # SAVE USER
    # ======================================

    await (

        MessageService
        .create(

            db,

            {

                "conversation_id":
                body.conversation_id,

                "role":
                "user",

                "content":
                body.question,

            }

        )

    )

    rag_service = RagService()
    
    
    workscpace_code = PromptCode.HELPDESK.value

    answer = await (

        rag_service.ask(

            db=db,

            conversation_id=
            body.conversation_id,

            question=
            body.question,

            chunks=
            chunks,

            model_id=
            body.model_id,

            mode=
            body.mode,
            
            workspace_code=
            workscpace_code,

        )

    )

    # ======================================
    # BUILD SOURCES
    # ======================================

    if body.mode == PromptCode.PUBLIC:

        result = json.loads(
            answer
        )

        answer = result["answer"]

        sources = result["sources"]

    else:

        source_map = {}

        for chunk in chunks:

            file = chunk["source_file"]

            if file not in source_map:

                source_map[file] = {

                    "source_file":
                    file,
                    
                    "source_url": chunk["source_url"],

                    "excerpt":
                    chunk["content"],

                    "type":
                    "internal",

                }

        sources = list(
            source_map.values()
        )

    # ======================================
    # SAVE ASSISTANT
    # ======================================

    await (

        MessageService
        .create(

            db,

            {

                "conversation_id":
                body.conversation_id,

                "role":
                "assistant",

                "content":
                answer,

            }

        )

    )

    # await (
    #     ConversationSummaryService
    #     .update_summary(
    #         db=db,
    #         conversation_id=body.conversation_id,
    #     )
    # )

    return {

        "conversation_id":
        str(body.conversation_id),

        "title":
        body.question,

        "answer":
        answer,

        "sources":
        sources,

    }