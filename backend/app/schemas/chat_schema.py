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
    conversation_id:str

    question:str


    


    role_id:int
    
    model_id:str


class ChatResponse(

    BaseModel

):

    answer:str


    email:str


    role:str


    chunks:list[Any]