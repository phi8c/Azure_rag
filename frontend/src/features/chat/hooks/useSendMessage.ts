import {

useMutation,
useQueryClient


}

from "@tanstack/react-query";


import {

sendMessage,

type ChatRequest,

type ChatResponse

}


from "../api/chat.api";


import {

useChatStore

}

from "../store/chat.store";


export function useSendMessage(){

const queryClient=

useQueryClient();

 const addMessage=

 useChatStore(

  s=>s.addMessage

 );


 return useMutation<

 ChatResponse,

 Error,

 ChatRequest

 >({

 mutationFn:

 sendMessage,


onSuccess:()=>{

 queryClient.invalidateQueries({

   queryKey:

   ["messages"]

 })

}

 })

}