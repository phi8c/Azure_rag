import {

useEffect

}

from "react";

import {

useQuery

}

from "@tanstack/react-query";

import {

getConversations

}

from "../api/conversation.api";

import {

useChatStore

}

from "../store/chat.store";


export function useConversation(

 email:string

){

 const setConversations=

 useChatStore(

 s=>s.setConversations

 );

 const currentConversationId=

 useChatStore(

 s=>s.currentConversationId

 );

 const setCurrentConversation=

 useChatStore(

 s=>s.setCurrentConversation

 );

 const query=

 useQuery({

 queryKey:

 ["conversations",email],

 queryFn:

 ()=>

 getConversations(

  email

 )

 });


 useEffect(()=>{

 if(

  query.data

 ){

  setConversations(

    query.data

  );

  if(

    !currentConversationId &&

    query.data.length > 0

  ){

    setCurrentConversation(

      query.data[0].id

    );

  }

 }

 },[

 query.data,

 currentConversationId,

 setConversations,

 setCurrentConversation

 ]);


 return query;
}