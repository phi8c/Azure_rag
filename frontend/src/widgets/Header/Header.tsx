import { Bell, ShieldCheck, Sparkles } from "lucide-react";

export default function Header() {
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

        <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
          <button
            style={{
              background: "none",
              border: "none",
              cursor: "pointer",
              width: "36px",
              height: "36px",
              borderRadius: "50%",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              color: "#444746",
              position: "relative",
              transition: "background-color 0.2s"
            }}
            onMouseEnter={(e) => (e.currentTarget.style.backgroundColor = "#f1f3f4")}
            onMouseLeave={(e) => (e.currentTarget.style.backgroundColor = "transparent")}
          >
            <Bell size={20} />
            <span
              style={{
                position: "absolute",
                top: "8px",
                right: "8px",
                width: "8px",
                height: "8px",
                backgroundColor: "#ea4335",
                borderRadius: "50%",
                border: "2px solid #ffffff"
              }}
            />
          </button>
        </div>
      </header>
    </div>
  );
}