import { Send, Image, Mic } from "lucide-react";

type Props = {
  value: string;
  onChange: (value: string) => void;
  onSubmit: () => void;
};

export default function PromptInput({ value, onChange, onSubmit }: Props) {
  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter" && !e.shiftKey && value.trim()) {
      onSubmit();
    }
  };

  const hasValue = value.trim().length > 0;

  return (
    <div
      style={{
        padding: "16px 24px",
        backgroundColor: "#ffffff",
        width: "100%",
        boxSizing: "border-box",
        fontFamily: "Segoe UI, Tahoma, Geneva, Verdana, sans-serif"
      }}
    >
      <div style={{ maxWidth: "850px", margin: "0 auto" }}>
        <div
          style={{
            display: "flex",
            flexDirection: "column",
            borderRadius: "28px",
            backgroundColor: "#f0f4f9",
            padding: "8px 16px 8px 24px",
            transition: "background-color 0.2s, box-shadow 0.2s",
            boxShadow: "none"
          }}
          onFocus={(e) => {
            e.currentTarget.style.backgroundColor = "#ffffff";
            e.currentTarget.style.boxShadow = "0 1px 3px 1px rgba(60,64,67,.15), 0 1px 2px 0 rgba(60,64,67,.30)";
          }}
          onBlur={(e) => {
            e.currentTarget.style.backgroundColor = "#f0f4f9";
            e.currentTarget.style.boxShadow = "none";
          }}
        >
          <div style={{ display: "flex", alignItems: "center", width: "100%" }}>
            <input
              value={value}
              onChange={(e) => onChange(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Nhập câu lệnh tại đây"
              style={{
                flex: 1,
                backgroundColor: "transparent",
                border: "none",
                outline: "none",
                fontSize: "16px",
                color: "#1f1f1f",
                padding: "12px 0",
                minWidth: "0"
              }}
            />

            <div style={{ display: "flex", alignItems: "center", gap: "4px", marginLeft: "12px", flexShrink: 0 }}>
              <button
                type="button"
                style={{
                  background: "none",
                  border: "none",
                  cursor: "pointer",
                  width: "40px",
                  height: "40px",
                  borderRadius: "50%",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  color: "#444746",
                  transition: "background-color 0.2s"
                }}
                onMouseEnter={(e) => (e.currentTarget.style.backgroundColor = "#e1e5ea")}
                onMouseLeave={(e) => (e.currentTarget.style.backgroundColor = "transparent")}
              >
                <Image size={20} />
              </button>

              <button
                type="button"
                style={{
                  background: "none",
                  border: "none",
                  cursor: "pointer",
                  width: "40px",
                  height: "40px",
                  borderRadius: "50%",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  color: "#444746",
                  transition: "background-color 0.2s"
                }}
                onMouseEnter={(e) => (e.currentTarget.style.backgroundColor = "#e1e5ea")}
                onMouseLeave={(e) => (e.currentTarget.style.backgroundColor = "transparent")}
              >
                <Mic size={20} />
              </button>

              <button
                onClick={onSubmit}
                disabled={!hasValue}
                style={{
                  background: "none",
                  border: "none",
                  cursor: hasValue ? "pointer" : "default",
                  width: "40px",
                  height: "40px",
                  borderRadius: "50%",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  color: hasValue ? "#1a73e8" : "#c4c7c5",
                  transition: "background-color 0.2s, color 0.2s"
                }}
                onMouseEnter={(e) => {
                  if (hasValue) e.currentTarget.style.backgroundColor = "#e1e5ea";
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.backgroundColor = "transparent";
                }}
              >
                <Send size={20} />
              </button>
            </div>
          </div>
        </div>

        <p
          style={{
            fontSize: "12px",
            color: "#444746",
            textAlign: "center",
            marginTop: "12px",
            marginBottom: "0",
            userSelect: "none",
            letterSpacing: "0.1px"
          }}
        >
          Gemini có thể đưa ra thông tin không chính xác, kể cả về con người, vì vậy hãy xác minh các câu trả lời.
        </p>
      </div>
    </div>
  );
}