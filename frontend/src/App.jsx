import { useState } from "react";
import ChatBox from "./components/ChatBox";
import "./App.css";

export default function App() {
const [agent, setAgent] = useState("auto");

const [chats, setChats] = useState([
{
id: 1,
title: "New Chat",
messages: [],
},
]);

const [activeChat, setActiveChat] = useState(1);

const currentChat =
chats.find((c) => c.id === activeChat) || chats[0];

const updateMessages = (messages) => {
setChats((prev) =>
prev.map((chat) =>
chat.id === activeChat
? {
...chat,
messages,
title:
chat.title === "New Chat" &&
messages.length > 0
? messages[0].text.slice(0, 25)
: chat.title,
}
: chat
)
);
};

const newChat = () => {
  const newId = Date.now();

  const newConversation = {
    id: newId,
    title: "New Chat",
    messages: [],
  };

  setChats((prev) => [
    ...prev,
    newConversation,
  ]);

  setActiveChat(newId);
};

return ( <div className="app-container">


  {/* SIDEBAR */}
  <div className="sidebar">

    <div className="sidebar-logo">
      🚀 DevBuddy
    </div>


    {/* AGENTS */}
    <div className="agents-section">

      <h4>Agents</h4>

      <button
        className={`agent-btn ${
          agent === "auto" ? "active-agent" : ""
        }`}
        onClick={() => setAgent("auto")}
      >
        🤖 Auto Team
      </button>

      <button
        className={`agent-btn ${
          agent === "product" ? "active-agent" : ""
        }`}
        onClick={() => setAgent("product")}
      >
        👨‍💼 Product Manager
      </button>

      <button
        className={`agent-btn ${
          agent === "architect" ? "active-agent" : ""
        }`}
        onClick={() => setAgent("architect")}
      >
        🏗 Architect
      </button>

      <button
        className={`agent-btn ${
          agent === "backend" ? "active-agent" : ""
        }`}
        onClick={() => setAgent("backend")}
      >
        ⚙ Backend Engineer
      </button>

      <button
        className={`agent-btn ${
          agent === "frontend" ? "active-agent" : ""
        }`}
        onClick={() => setAgent("frontend")}
      >
        🎨 Frontend Engineer
      </button>

      <button
        className={`agent-btn ${
          agent === "devops" ? "active-agent" : ""
        }`}
        onClick={() => setAgent("devops")}
      >
        ☁ DevOps Engineer
      </button>
      <button
      className="new-chat-btn"
      onClick={newChat}
    >
      + New Chat
    </button>
    </div>

    {/* HISTORY */}
    <div className="history-section">
  {chats.map((chat) => (
    <div
      key={chat.id}
      className={`chat-item ${
        chat.id === activeChat ? "active" : ""
      }`}
    >
      <span
        onClick={() => setActiveChat(chat.id)}
      >
        {chat.title}
      </span>

      <button
        className="delete-btn"
        onClick={() => {
  const updated = chats.filter(
    (c) => c.id !== chat.id
  );

  setChats(updated);

  if (updated.length > 0) {
    setActiveChat(updated[0].id);
  } else {
    const newId = Date.now();

    setChats([
      {
        id: newId,
        title: "New Chat",
        messages: [],
      },
    ]);

    setActiveChat(newId);
  }
}}
      >
        ×
      </button>
    </div>
  ))}
</div>

</div>

{/* CHAT AREA */}
<div className="chat-area">
  <ChatBox
    messages={currentChat?.messages || []}
    setMessages={updateMessages}
    agent={agent}
  />
</div>

</div>
);
}