import { useState } from "react";

export default function ChatInput({ sendMessage }) {
  const [text, setText] = useState("");

  const handleSend = () => {
    if (!text.trim()) return;
    sendMessage(text);
    setText("");
  };

  return (
    <div className="p-4 bg-gray-900 flex gap-2">
      <input
        className="flex-1 p-2 rounded bg-gray-800 outline-none"
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="Ask something..."
      />

      <button
        onClick={handleSend}
        className="bg-green-600 px-4 py-2 rounded"
      >
        Send
      </button>
    </div>
  );
}