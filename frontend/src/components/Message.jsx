export default function Message({ msg }) {
  return (
    <div
      className={`p-3 rounded max-w-lg ${
        msg.role === "user"
          ? "bg-blue-600 ml-auto"
          : "bg-gray-800 mr-auto"
      }`}
    >
      {msg.text}
    </div>
  );
}