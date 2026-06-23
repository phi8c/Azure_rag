import {  ShieldCheck, Sparkles } from "lucide-react";

import {useState} from "react"

import { useChatStore }
from "../../features/chat/store/chat.store";

import {
  activateSEF
}
from "../../features/graph/api/graph.api";

export default function Header() {



  const {

    useGraph,

    setUseGraph

  } = useChatStore();

  
const [loadingSEF, setLoadingSEF] =
  useState(false);


  return (
    <div
      style={{
        width: "100%",
        backgroundColor: "#ffffff",
        borderBottom: "1px solid #e1e5ea"
      }}
    >
      <header
        style={{
          height: "64px",
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          width: "100%",
          maxWidth: "850px",
          margin: "0 auto",
          padding: "0 24px",
          boxSizing: "border-box",
          fontFamily: "Segoe UI, Tahoma, Geneva, Verdana, sans-serif"
        }}
      >
        <div style={{ display: "flex", alignItems: "center", gap: "12px", paddingLeft: "40px" }}>
          <div
            style={{
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              width: "28px",
              height: "28px",
              borderRadius: "8px",
              backgroundColor: "#e3eefc"
            }}
          >
            <Sparkles size={16} style={{ color: "#1a73e8" }} />
          </div>
          
          <div>
            <h1
              style={{
                margin: 0,
                fontSize: "16px",
                fontWeight: "600",
                color: "#1f1f1f",
                letterSpacing: "0.3px"
              }}
            >
               RAG
            </h1>
          </div>
          
          <div
            style={{
              display: "flex",
              alignItems: "center",
              gap: "6px",
              backgroundColor: "#e6f4ea",
              padding: "4px 8px",
              borderRadius: "100px"
            }}
          >
            <ShieldCheck size={14} style={{ color: "#137333" }} />
            <span style={{ fontSize: "11px", fontWeight: "600", color: "#137333" }}>
              Trực tuyến
            </span>
          </div>
        </div>

        <div
  style={{
    display: "flex",
    alignItems: "center",
    gap: "12px"
  }}
>
  <span
    style={{
      fontSize: "12px",
      fontWeight: 600,
      color: useGraph
        ? "#137333"
        : "#666"
    }}
  >
    Graph Think
  </span>

  <label
    style={{
      position: "relative",
      display: "inline-block",
      width: "44px",
      height: "24px",
      cursor: "pointer"
    }}
  >
    <input
      type="checkbox"
      checked={useGraph}
      onChange={(e) =>

        setUseGraph(
          e.target.checked
        )
      }
      style={{
        display: "none"
      }}
    />

    <span
      style={{
        position: "absolute",
        inset: 0,
        backgroundColor: useGraph
          ? "#1a73e8"
          : "#ccc",
        borderRadius: "999px",
        transition: "0.2s"
      }}
    />

    <span
      style={{
        position: "absolute",
        top: "2px",
        left: useGraph
          ? "22px"
          : "2px",
        width: "20px",
        height: "20px",
        backgroundColor: "#fff",
        borderRadius: "50%",
        transition: "0.2s"
      }}
    />
  </label>
</div>

<button
  onClick={async () => {

    try {

      setLoadingSEF(
        true
      );

      await activateSEF();

      alert(
`🧠 Self Embodiment of Perfection Activated

Bạn đã kích hoạt khả năng tự hoàn thiện cho Knowledge Graph thành công.

Hệ thống sẽ tự động phân tích các thực thể hiện có, khám phá những mối liên hệ tiềm ẩn và mở rộng mạng tri thức theo thời gian.

Quá trình này có thể kéo dài từ vài phút đến nhiều giờ tùy thuộc vào kích thước Graph.

Bạn có thể tiếp tục sử dụng hệ thống bình thường trong khi quá trình tự hoàn thiện đang diễn ra.`
      );

    } catch {

      alert(
        "Không thể kích hoạt Self Embodiment."
      );

    } finally {

      setLoadingSEF(
        false
      );

    }

  }}

  disabled={loadingSEF}

  style={{
    border: "none",
    cursor: "pointer",
    borderRadius: "10px",
    padding: "8px 12px",
    background:
      "#7c3aed",
    color: "#fff",
    fontSize: "12px",
    fontWeight: 600
  }}
>
  {
    loadingSEF

      ? "Activating..."

      : "🧠 Active SEF"
  }
</button>



      </header>
    </div>
  );
}