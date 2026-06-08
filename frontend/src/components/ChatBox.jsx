import { useState, useEffect, useRef } from "react";
import axios from "axios";
import ReactMarkdown from "react-markdown";

const ChatBox = ({
  messages,
  setMessages,
  agent
}) => {
  const [copiedIndex, setCopiedIndex] = useState(null);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const messagesEndRef = useRef(null);
  const copyToClipboard = (text, index) => {
    navigator.clipboard.writeText(text);

    setCopiedIndex(index);

    setTimeout(() => {
      setCopiedIndex(null);
    }, 2000);
  };
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [messages, loading]);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMsg = {
      role: "user",
      text: input,
    };

    const updated = [...messages, userMsg];

    setMessages(updated);
    setInput("");

    try {
      setLoading(true);

      const res = await axios.post(
        "http://127.0.0.1:8000/chat",
        {
          query: input,
          agent: agent,
        }
      );

      const aiMsg = {
        role: "ai",
        text: res.data.response,
      };

      setMessages([
        ...updated,
        aiMsg,
      ]);
    } catch (err) {
      setMessages([
        ...updated,
        {
          role: "ai",
          text: "❌ Backend Error",
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (
      e.key === "Enter" &&
      !e.shiftKey
    ) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <div className="chat-wrapper">

      {/* HEADER */}
      <div className="chat-header">

        <div>
          🚀 DevBuddy 
        </div>
        <div className="download-actions">
  <div className="download-bar">
  <button onClick={() => window.open("http://127.0.0.1:8000/download/pdf")}>
    📄 PDF Report
  </button>

 
</div>
</div>

        <div className="agent-badge">
          {agent === "auto" && "🤖 Auto Team"}
          {agent === "product" && "👨‍💼 Product Manager"}
          {agent === "architect" && "🏗 Architect"}
          {agent === "backend" && "⚙ Backend Engineer"}
          {agent === "frontend" && "🎨 Frontend Engineer"}
          {agent === "devops" && "☁ DevOps Engineer"}
        </div>

      </div>

      {/* MESSAGES */}
      <div className="chat-messages">

        {messages.length === 0 ? (
          <div className="welcome-screen">

            <h1>🚀 DevBuddy</h1>

            <p>
              Your AI Software Engineer &
              System Architect
            </p>

            <div className="suggestions">

              <button
                onClick={() =>
                  setInput("Build a FastAPI CRUD API")
                }
              >
                Build API
              </button>

              <button
                onClick={() =>
                  setInput("Debug this React code")
                }
              >
                Debug Code
              </button>

              <button
                onClick={() =>
                  setInput("Design a scalable system")
                }
              >
                System Design
              </button>

              <button
                onClick={() =>
                  setInput("Generate a React component")
                }
              >
                Generate UI
              </button>

            </div>
          </div>
        ) : (
          <>
            {messages.map((msg, i) => (
              <div
                key={i}
                className={`message ${
                  msg.role === "user"
                    ? "user"
                    : "ai"
                }`}
              >
                {msg.role === "ai" ? (
  <div className="message-content">

    <button
      className="copy-btn"
      onClick={() =>
        copyToClipboard(msg.text, i)
      }
    >
      {copiedIndex === i
        ? "✅ Copied"
        : "📋 Copy"}
    </button>

    <ReactMarkdown>
      {msg.text}
    </ReactMarkdown>

  </div>
) : (
                  <div>{msg.text}</div>
                )}
              </div>
            ))}

            {loading && (
              <div className="message ai typing">
                <span></span>
                <span></span>
                <span></span>
              </div>
            )}
          </>
        )}

        <div ref={messagesEndRef}></div>

      </div>

      {/* INPUT */}
      <div className="chat-input">

        <input
          type="text"
          value={input}
          placeholder="Ask DevBuddy anything..."
          onChange={(e) =>
            setInput(e.target.value)
          }
          onKeyDown={handleKeyDown}
        />

        <button onClick={sendMessage}>
          Send
        </button>

      </div>

    </div>
  );
};

export default ChatBox;