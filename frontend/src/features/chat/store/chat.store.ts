import { create }
from "zustand";

import type {
 Message
}
from "../types/message";

import type {
 Conversation
}
from "../types/conversation";


type ChatState = {

 messages:
 Message[];

 conversations:
 Conversation[];

 currentConversationId:
 string | null;



 


 setMessages:
 (
   messages:Message[]
 )=>void;


 addMessage:
 (
   message:Message
 )=>void;


 setConversations:
 (
   conversations:
   Conversation[]
 )=>void;


 setCurrentConversation:
 (
   id:string
 )=>void;


 renameConversation:
(
  id: string,
  title: string
)=>void;

};




export const useChatStore=

create<ChatState>(

(set)=>({

messages:[],

conversations:[],

currentConversationId:
null,




setMessages:
(messages)=>

set({

messages

}),


addMessage:
(message)=>

set(

(state)=>({

messages:[

...state.messages,

message

]

})

),  




renameConversation: (
  id: string,
  title: string
) =>

set(state => ({

  conversations:

  state.conversations.map(

    conversation =>

    conversation.id === id

      ? {
          ...conversation,
          title
        }

      : conversation

  )

})),


setConversations:
(conversations)=>

set({

conversations

}),


setCurrentConversation:
(id)=>

set({

currentConversationId:
id

})

})

)