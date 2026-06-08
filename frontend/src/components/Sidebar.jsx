import { FiPlus } from "react-icons/fi";

export default function Sidebar({
  chats,
  activeChat,
  setActiveChat,
  setChats,
}) {
  const newChat = () => {
    const newId = Date.now();
    setChats([...chats, { id: newId, title: "New Chat" }]);
    setActiveChat(newId);
  };

  return (
    <div className="w-64 bg-gray-900 p-4 flex flex-col">
      <button
        onClick={newChat}
        className="flex items-center gap-2 bg-green-600 hover:bg-green-700 p-2 rounded"
      >
        <FiPlus /> New Chat
      </button>

      <div className="mt-4 space-y-2">
        {chats.map((chat) => (
          <div
            key={chat.id}
            onClick={() => setActiveChat(chat.id)}
            className={`p-2 rounded cursor-pointer ${
              activeChat === chat.id ? "bg-gray-700" : "hover:bg-gray-800"
            }`}
          >
            {chat.title}
          </div>
        ))}
      </div>
    </div>
  );
}