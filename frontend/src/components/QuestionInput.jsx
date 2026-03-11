import { useState } from "react";

function QuestionInput({ onSend, loading }) {
  const [question, setQuestion] = useState("");

  const handleSend = () => {
    if (!question.trim() || loading) return;

    onSend(question);
    setQuestion("");
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter") {
      handleSend();
    }
  };

  return (
    <div style={{ display: "flex", gap: "10px", marginTop: "16px" }}>
      <input
        type="text"
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        onKeyDown={handleKeyDown}
        placeholder="Ask your campus question..."
        style={{
          flex: 1,
          padding: "14px",
          borderRadius: "10px",
          border: "1px solid #cbd5e1",
          outline: "none",
          fontSize: "15px",
        }}
      />

      <button
        onClick={handleSend}
        disabled={loading}
        style={{
          padding: "14px 22px",
          borderRadius: "10px",
          border: "none",
          background: loading ? "#94a3b8" : "#2563eb",
          color: "white",
          cursor: loading ? "not-allowed" : "pointer",
          fontWeight: "bold",
        }}
      >
        Send
      </button>
    </div>
  );
}

export default QuestionInput;