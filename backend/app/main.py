from fastapi import FastAPI

from app.api.v1.role_router import router as role_router
from app.api.v1.tag_router import router as tag_router

from app.api.v1.tag_role_rule_router import (
    router as tag_role_rule_router
)
from app.api.v1.policy_router import (
    router as policy_router
)
from app.api.v1.chunk_router import (
    router as chunk_router
)

from app.api.v1.chat_router import (
    router as chat_router
)

from app.api.v1.permission_router import (
    router as permission_router
)
from app.api.v1.bot_router import (

    router as bot_router

)
from app.api.v1.conversation_router import (
    router as conversation
)
from app.api.v1.document_router import (
    router as document_router
)

from fastapi.middleware.cors import (

    CORSMiddleware

)








app = FastAPI(

    title=
    "chatrag",


    version=
    "1.0",


    servers=[

        {

            "url":

            "https://unwell-kinsman-legwork.ngrok-free.dev",


            "description":

            "Ngrok public API"

        }

    ]

)


app.add_middleware(

    CORSMiddleware,

    allow_origins=[

        "http://localhost:5173"

    ],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"]

)

app.include_router(role_router)
app.include_router(tag_router)
app.include_router(tag_role_rule_router)
app.include_router(policy_router)
app.include_router(chunk_router)
app.include_router(chat_router)
app.include_router(permission_router)
app.include_router(bot_router)
app.include_router(conversation)
app.include_router(document_router)