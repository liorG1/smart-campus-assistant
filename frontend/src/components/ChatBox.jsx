import { useEffect, useRef, useState } from "react";
import Message from "./Message";
import QuestionInput from "./QuestionInput";

function ChatBox() {
  const [messages, setMessages] = useState([
    {
      text: "Hello, how can I help you with campus information today?",
      sender: "ai",
    },
  ]);
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  const sendQuestion = async (question) => {
    const userMessage = { text: question, sender: "user" };
    setMessages((prev) => [...prev, userMessage]);
    setLoading(true);

    try {
      const response = await fetch("http://localhost:8000/ask", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ question }),
      });

      if (!response.ok) {
        throw new Error(`Request failed with status ${response.status}`);
      }

      const data = await response.json();

      const aiMessage = {
        text: data.answer || "No answer returned from server",
        sender: "ai",
      };

      setMessages((prev) => [...prev, aiMessage]);
    } catch (error) {
      console.error("Error while fetching answer:", error);

      setMessages((prev) => [
        ...prev,
        {
          text: "AI service is temporarily unavailable.",
          sender: "ai",
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div
      style={{
        maxWidth: "700px",
        margin: "0 auto",
        background: "white",
        borderRadius: "16px",
        boxShadow: "0 8px 30px rgba(0,0,0,0.08)",
        padding: "20px",
      }}
    >
      <div
        style={{
          height: "420px",
          overflowY: "auto",
          border: "1px solid #e2e8f0",
          borderRadius: "12px",
          padding: "16px",
          background: "#f8fafc",
        }}
      >
        {messages.map((msg, index) => (
          <Message key={index} text={msg.text} sender={msg.sender} />
        ))}

        {loading && (
          <div style={{ textAlign: "left", marginTop: "10px", color: "#64748b" }}>
            AI is thinking...
          </div>
        )}

        <div ref={bottomRef} />
      </div>

      <QuestionInput onSend={sendQuestion} loading={loading} />
    </div>
  );
}

export default ChatBox;