import type { Message } from "../types/message";

type Props = {
  message: Message;
};

export default function MessageBubble({ message }: Props) {
  const isUser = message.role === "user";

  return (
    <div
      style={{
        display: "flex",
        width: "100%",
        marginBottom: "32px",
        justifyContent: isUser ? "flex-end" : "flex-start",
        paddingLeft: isUser ? "48px" : "0",
        paddingRight: isUser ? "0" : "48px",
        boxSizing: "border-box",
        fontFamily: "Segoe UI, Tahoma, Geneva, Verdana, sans-serif"
      }}
    >
      <div
        style={{
          display: "flex",
          gap: "16px",
          maxWidth: "100%",
          alignItems: "flex-start",
          flexDirection: isUser ? "row-reverse" : "row"
        }}
      >
        <div
          style={{
            height: "32px",
            width: "32px",
            borderRadius: "50%",
            flexShrink: 0,
            background: isUser 
              ? "linear-gradient(to top right, #38bdf8, #34d399)" 
              : "linear-gradient(135deg, #4285f4, #9b51e0, #ea4335)",
            display: "flex",
            alignItems: "center",
            justifyContent: "center"
          }}
        />

        <div
          style={{
            backgroundColor: isUser ? "#f0f4f9" : "transparent",
            color: "#1f1f1f",
            borderRadius: isUser ? "18px" : "0px",
            padding: isUser ? "12px 20px" : "4px 0px",
            fontSize: "15px",
            lineHeight: "1.6",
            whiteSpace: "pre-wrap",
            wordBreak: "break-word",
            maxWidth: isUser ? "750px" : "100%"
          }}
        >
          {message.content}
        </div>
      </div>
    </div>
  );
}