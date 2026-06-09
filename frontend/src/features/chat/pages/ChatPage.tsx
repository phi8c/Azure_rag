import { useEffect, useState } from "react";

import MainLayout from "@/app/layouts/MainLayout";
import ChatPanel from "@/widgets/ChatPanel/ChatPanel";

import PromptInput from "../components/PromptInput";
import MessageList from "../components/MessageList";

import { useChatStore } from "../store/chat.store";

import { useSendMessage } from "../hooks/useSendMessage";
import { useMessages } from "../hooks/useMessages";

import { getConversationSummary } from "../api/conversation.api";

import { useMsal } from "@azure/msal-react";


import {
  renameConversation
}
from "../api/conversation.api";
export default function ChatPage() {

  const { instance } = useMsal();

  const [role, setRole] =
    useState("");

  const [summary, setSummary] =
    useState("");

  const [showSummary, setShowSummary] =
    useState(false);

  const [message, setMessage] =
    useState("");

  const messages =
    useChatStore(
      s => s.messages
    );

  const currentConversationId =
    useChatStore(
      s => s.currentConversationId
    );

  const addMessage =
    useChatStore(
      s => s.addMessage
    );

  const account =
    instance.getActiveAccount();

  useMessages(
    currentConversationId ??
    undefined
  );


  const renameConversationStore =
useChatStore(
  s => s.renameConversation
);

  const {
    mutateAsync,
   
  } = useSendMessage();

  useEffect(() => {

    if (!currentConversationId)
      return;

    const run = async () => {

      try {

        const res =
          await getConversationSummary(
            currentConversationId
          );

        if (
          res?.summary &&
          res.summary.trim()
        ) {

          setSummary(
            res.summary
          );

          setShowSummary(
            true
          );

        }

      } catch (error) {

        // console.error(
        //   "summary error",
        //   error
        // );

      }

    };

    run();

  }, [
    currentConversationId
  ]);

  useEffect(() => {

    if (!showSummary)
      return;

    const timer =
      setTimeout(() => {

        setShowSummary(
          false
        );

      }, 20000);

    return () =>
      clearTimeout(timer);

  }, [showSummary]);

  useEffect(() => {

    const run = async () => {

      const account =
        instance.getActiveAccount();

      if (!account)
        return;

      const token =
        await instance.acquireTokenSilent({
          account,
          scopes: [
            "User.Read",
            "GroupMember.Read.All"
          ]
        });

      const response =
        await fetch(
          "https://graph.microsoft.com/v1.0/me/memberOf?$select=id,displayName",
          {
            headers: {
              Authorization:
                `Bearer ${token.accessToken}`
            }
          }
        );

      const data =
        await response.json();

      setRole(
        data.value?.[0]?.displayName ?? ""
      );

      console.log(
        "GRAPH",
        data
      );

    };

    run();

  }, []);

  async function handleSubmit() {


    const isFirstMessage =
  messages.length === 0;

    if (
      !message.trim() ||
      !currentConversationId
    )
      return;

    const content =
      message;

    setMessage("");

    addMessage({

      id:
        crypto.randomUUID(),

      role:
        "user",

      content,

      createdAt:
        new Date()
          .toISOString()

    });

    await mutateAsync({
  conversation_id:
    currentConversationId,
  question:
    content,
  role,
  email:
    account?.username ?? ""
});

if (isFirstMessage) {

  const newTitle =
    content.length > 50
      ? content.slice(0, 50) + "..."
      : content;

  await renameConversation(
    currentConversationId,
    newTitle
  );

  renameConversationStore(
    currentConversationId,
    newTitle
  );
}
 
  }

  return (

    <>

      {
        showSummary && (

          <div
  style={{
    position: "fixed",
    top: "20px",
    right: "20px",
    width: "400px",
    background: "#ffffff",
    color: "#1f2937",
    padding: "16px",
    borderRadius: "12px",
    boxShadow:
      "0 4px 20px rgba(0,0,0,0.2)",
    zIndex: 9999
  }}
>

            <h3>
              📌 Tóm tắt hội thoại
            </h3>

            <p
  style={{
    color:"#374151"
  }}
>
              {summary}
            </p>

            <button
              onClick={() =>
                setShowSummary(false)
              }
            >
              Đóng
            </button>

          </div>

        )
      }

      <MainLayout>

        <ChatPanel>

          <div
            className="
            h-full
            flex
            flex-col
          "
          >

            <MessageList
              messages={messages}
            />

            <PromptInput
              value={message}
              onChange={setMessage}
              onSubmit={handleSubmit}
            />

          </div>

        </ChatPanel>

      </MainLayout>

    </>

  );

}