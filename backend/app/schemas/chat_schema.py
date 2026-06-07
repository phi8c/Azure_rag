from pydantic import (

    BaseModel

)

from typing import (

    Any

)

from uuid import UUID


class ChatRequest(

    BaseModel

):
    conversation_id:UUID

    question:str


    email:str


    role:str


class ChatResponse(

    BaseModel

):

    answer:str


    email:str


    role:str


    chunks:list[Any]