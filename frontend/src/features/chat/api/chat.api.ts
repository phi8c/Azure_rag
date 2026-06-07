import { api }
from "@/shared/api/axios";


export interface ChatRequest {


  conversation_id:string;

  question:string;

  role:string;

  email:string;

}


export interface ChatResponse {

  answer:string;

  chunks:any[];

  role:string;

  email:string;

}


export async function sendMessage(

 body:ChatRequest

):

Promise<ChatResponse>{

 const response=

 await api.post(

   "/chat/query",

   body

 );

//  console.log("in ra data", response.data)

 return response.data;

}