import { api }
from "@/shared/api/axios";

import type {
 Conversation
}
from "../types/conversation";


import type {

 Message

}

from "../types/message";


export async function getConversations(

 email:string

):

Promise<Conversation[]>

{

 const response=

 await api.get(

   `/conversations/${email}`

 );

 return response.data;

}


export async function

getMessages(

 conversationId:string

):

Promise<Message[]>

{

 const response=

 await api.get(

 `/conversations/${conversationId}/messages`

)

 return response.data;

}



export async function createConversation(

 email:string

){

 const response=

 await api.post(

   "/conversations",

   {

     email

   }

 );

 return response.data;

}

export async function getConversationSummary(
  conversationId: string
) {

  const response = await api.get(
    `/conversations/${conversationId}/summary`
  );

  return response.data;

}


export async function renameConversation(
  id: string,
  title: string
){

  const response =
    await api.patch(

      `/conversations/${id}`,

      null,

      {
        params: {
          title
        }
      }

    );

  return response.data;

}