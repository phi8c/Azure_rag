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

from app.schemas.chat_schema import (

    ChatRequest,

    ChatResponse

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

from app.services.message.message_service import (

 MessageService

)

from app.services.session_memory.session_memory_service import (

 SessionMemoryService

)
from app.services.session_memory.conversation_summary_service import (
    ConversationSummaryService
)


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


 permissions = await (

  PermissionRepository

  .get_role_access(

   db,

   body.role

  )

 )
 retrieval_query = await (
     SessionMemoryService
     .build_retrieval_query(
         db=db,
         conversation_id=body.conversation_id,
         question = body.question
     )
 )


 chunks = (

  AzureSearchService

  .retrieve(

   question=

   retrieval_query,

   permissions=

   permissions

  )

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


 answer = await (

  rag_service.ask(
    
   db=db,
   conversation_id=body.conversation_id,

   question=

   body.question,

   chunks=

   chunks

  )

 )


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
 
 await (
    ConversationSummaryService
    .update_summary(
        db=db,
        conversation_id=body.conversation_id
    )
)


 return {

  "answer":

  answer,

  "chunks":

  chunks,
   "conversation_id":

 body.conversation_id,


 }
 
 