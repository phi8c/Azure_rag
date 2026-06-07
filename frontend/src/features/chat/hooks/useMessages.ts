import {

useEffect

}

from "react";


import {

useQuery

}

from "@tanstack/react-query";


import {

getMessages

}

from "../api/conversation.api";


import {

useChatStore

}

from "../store/chat.store";


export function

useMessages(

 conversationId?:

 string

){

 const setMessages=

 useChatStore(

 s=>

 s.setMessages

 );


 const query=

 useQuery({

 queryKey:

 ["messages",

 conversationId],

 queryFn:

 ()=>

 getMessages(

  conversationId!

 ),

 enabled:

 !!conversationId

 });


 useEffect(()=>{

 if(

 query.data

 ){

 setMessages(

   query.data

 )

 }

 },[

 query.data

 ]);


 return query;
}