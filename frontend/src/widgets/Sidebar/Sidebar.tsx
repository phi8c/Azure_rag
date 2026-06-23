import { useState } from "react";
import {
  Menu,
  Network,
  BookOpen,
  Plus,
  Settings
} from "lucide-react";
import ConversationList from "@/features/chat/components/ConversationList";
import { useConversation } from "@/features/chat/hooks/useConversation";
import { useCreateConversation } from "@/features/chat/hooks/useCreateConversation";
import { useChatStore } from "@/features/chat/store/chat.store";
import { useMsal } from "@azure/msal-react";

import GraphModal
from "@/features/graph/components/GraphModal";

import LibraryModal
from "@/features/documents/components/LibraryModal";

export default function Sidebar() {
  const [open, setOpen] = useState(true);
  //const email = "abc@gmail.com";

  const { instance } = useMsal();

  const account =
  instance.getActiveAccount();

  const email =
  account?.username ?? "";

  useConversation(email);

  const [showLibrary, setShowLibrary] =
  useState(false);

  const [showGraph, setShowGraph] =
useState(false);

  const conversations = useChatStore(s => s.conversations);
  const activeId = useChatStore(s => s.currentConversationId);
  const setCurrentConversation = useChatStore(s => s.setCurrentConversation);
  const { mutateAsync } = useCreateConversation();

  async function handleCreateConversation() {
    const res = await mutateAsync(email);
    setCurrentConversation(res.id);
  }

  function handleSelect(id: string) {
    setCurrentConversation(id);
  }

  return (
    <>
    <aside
      style={{
        display: "flex",
        flexDirection: "column",
        height: "100vh",
        width: open ? "280px" : "68px",
        backgroundColor: "#f0f4f9",
        padding: "16px 12px",
        transition: "width 0.2s ease-in-out",
        boxSizing: "border-box",
        fontFamily: "Segoe UI, Tahoma, Geneva, Verdana, sans-serif",
        position: "relative"
      }}
    >
      <div style={{ display: "flex", alignItems: "center", height: "48px", paddingLeft: "4px" }}>
        <button
          onClick={() => setOpen(!open)}
          style={{
            background: "none",
            border: "none",
            cursor: "pointer",
            padding: "10px",
            borderRadius: "50%",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            color: "#444746"
          }}
          onMouseEnter={(e) => (e.currentTarget.style.backgroundColor = "#e1e5ea")}
          onMouseLeave={(e) => (e.currentTarget.style.backgroundColor = "transparent")}
        >
          <Menu size={20} />
        </button>
        {open && (
          <span style={{ fontSize: "22px", color: "#1f1f1f", marginLeft: "16px", fontWeight: "400" }}>
            Assistant RAG
          </span>
        )}
      </div>

      <div style={{ marginTop: "20px", paddingLeft: "4px" }}>
        <button
          onClick={handleCreateConversation}
          style={{
            display: "flex",
            alignItems: "center",
            justifyContent: open ? "flex-start" : "center",
            gap: "12px",
            borderRadius: "16px",
            backgroundColor: "#b3d7ff",
            color: "#041e49",
            border: "none",
            cursor: "pointer",
            width: open ? "auto" : "40px",
            height: "40px",
            padding: open ? "0 20px" : "0",
            fontSize: "14px",
            fontWeight: "500",
            transition: "all 0.2s"
          }}
          onMouseEnter={(e) => (e.currentTarget.style.backgroundColor = "#a3cdff")}
          onMouseLeave={(e) => (e.currentTarget.style.backgroundColor = "#b3d7ff")}
        >
          <Plus size={20} style={{ minWidth: "20px" }} />
          {open && <span style={{ whiteSpace: "nowrap" }}>Cuộc trò chuyện mới</span>}
        </button>
      </div>

      <div style={{ marginTop: "24px", display: "flex", flexDirection: "column", gap: "4px" }}>
        <button
  onClick={() => setShowGraph(true)}
  style={{
    display: "flex",
    alignItems: "center",
    justifyContent: open ? "flex-start" : "center",
    gap: "12px",
    borderRadius: "100px",
    color: "#1f1f1f",
    background: "none",
    border: "none",
    cursor: "pointer",
    width: "100%",
    height: "40px",
    padding: open ? "0 16px" : "0",
    fontSize: "14px",
    textAlign: "left"
  }}
>
  <Network size={20} />
  {open && (
    <span>
      Graph Visualize
    </span>
  )}
</button>

        <button
          style={{
            display: "flex",
            alignItems: "center",
            justifyContent: open ? "flex-start" : "center",
            gap: "12px",
            borderRadius: "100px",
            color: "#1f1f1f",
            background: "none",
            border: "none",
            cursor: "pointer",
            width: "100%",
            height: "40px",
            padding: open ? "0 16px" : "0",
            fontSize: "14px",
            textAlign: "left"
          }}
          onClick={() =>
            setShowLibrary(true)
          }
          onMouseEnter={(e) => (e.currentTarget.style.backgroundColor = "#e1e5ea")}
          onMouseLeave={(e) => (e.currentTarget.style.backgroundColor = "transparent")}
        >
           <BookOpen size={20} />
  {open && <span>Thư viện</span>}
        </button>
      </div>

      {open && (
        <div style={{ marginTop: "24px", padding: "0 16px" }}>
          <p style={{ fontSize: "14px", fontWeight: "500", color: "#1f1f1f", margin: "0 0 12px 0" }}>
            Số ghi chú
          </p>
          <button
            style={{
              display: "flex",
              alignItems: "center",
              gap: "12px",
              fontSize: "14px",
              color: "#1f1f1f",
              background: "none",
              border: "none",
              cursor: "pointer",
              padding: "0"
            }}
          >
            <Plus size={18} />
            <span>Sổ ghi chú mới</span>
          </button>
        </div>
      )}

      <div style={{ marginTop: "24px", flex: 1, overflowY: open ? "auto" : "hidden", width: "100%" }}>
        {open && (
          <p style={{ fontSize: "14px", fontWeight: "500", color: "#1f1f1f", margin: "0 0 8px 16px" }}>
            Gần đây
          </p>
        )}
        <div style={{ display: open ? "block" : "none" }}>
          <ConversationList
            conversations={conversations}
            activeId={activeId ?? ""}
            onSelect={handleSelect}
          />
        </div>
      </div>

      <div style={{ marginTop: "auto", display: "flex", flexDirection: "column", gap: "4px", width: "100%" }}>
        <div
          style={{
            display: "flex",
            alignItems: "center",
            justifyContent: open ? "flex-start" : "center",
            gap: "12px",
            borderRadius: "100px",
            cursor: "pointer",
            height: "40px",
            padding: open ? "0 12px" : "0"
          }}
          onMouseEnter={(e) => (e.currentTarget.style.backgroundColor = "#e1e5ea")}
          onMouseLeave={(e) => (e.currentTarget.style.backgroundColor = "transparent")}
        >
          <div
            style={{
              height: "24px",
              width: "24px",
              borderRadius: "50%",
              background: "linear-gradient(to top right, #38bdf8, #34d399)",
              flexShrink: 0
            }}
          />
          {open && (
            <span style={{ fontSize: "14px", fontWeight: "500", color: "#1f1f1f", overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>
              {email || "Đang tải..."}
            </span>
          )}
        </div>

        <button
          style={{
            display: "flex",
            alignItems: "center",
            justifyContent: open ? "flex-start" : "center",
            gap: "12px",
            borderRadius: "100px",
            color: "#1f1f1f",
            background: "none",
            border: "none",
            cursor: "pointer",
            width: "100%",
            height: "40px",
            padding: open ? "0 16px" : "0",
            fontSize: "14px",
            textAlign: "left"
          }}
          onMouseEnter={(e) => (e.currentTarget.style.backgroundColor = "#e1e5ea")}
          onMouseLeave={(e) => (e.currentTarget.style.backgroundColor = "transparent")}
        >
          <Settings size={20} style={{ minWidth: "20px" }} />
          {open && <span>Cài đặt</span>}
        </button>
      </div>
    </aside>
     {
      showLibrary && (

        <LibraryModal

          onClose={() =>
            setShowLibrary(false)
          }

        />

      )
      
    },
    {
      showGraph && (

    <GraphModal
  open={showGraph}
  onClose={() =>
    setShowGraph(false)
  }
  
/>
      )
}
    </>
  );  
}