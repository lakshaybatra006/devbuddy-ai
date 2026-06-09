const GOOGLE_LOGIN_URL =
  "https://devbuddy-ai-1.onrender.com/auth/google/login";

export default function Login({ onLoginSuccess }) {
  const handleLogin = () => {
    // redirect to backend
    window.location.href = GOOGLE_LOGIN_URL;
  };

  return (
    <div className="login-container">
      <div className="login-box">

        <h1>DevBuddy AI</h1>

        <button className="google-btn" onClick={handleLogin}>
          Login with Google
        </button>

      </div>
    </div>
  );
}