function Message({ text, sender }) {
  const isUser = sender === "user";

  return (
    <div
      style={{
        display: "flex",
        justifyContent: isUser ? "flex-end" : "flex-start",
        margin: "10px 0",
      }}
    >
      <div
        style={{
          maxWidth: "75%",
          padding: "12px 16px",
          borderRadius: "16px",
          background: isUser ? "#2563eb" : "#e2e8f0",
          color: isUser ? "white" : "#0f172a",
          textAlign: "left",
          lineHeight: "1.5",
          whiteSpace: "pre-wrap",
        }}
      >
        {text}
      </div>
    </div>
  );
}

export default Message;