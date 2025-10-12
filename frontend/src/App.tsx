import { useState } from "react";
import GoogleLoginButton from "./components/GoogleLoginButton";
import { getMe } from "./api";

interface User {
  name: string;
  email: string;
  [key: string]: any;
}

interface LoginResponse {
  token: string;
  user: User;
}

function App() {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);

  const handleLogin = async (data: LoginResponse) => {
    setToken(data.token);
    setUser(data.user);
  };

  const handleCheck = async () => {
    if (!token) return;
    const me = await getMe(token);
    alert(JSON.stringify(me, null, 2));
  };

  return (
    <div style={{ padding: 40 }}>
      <h2>Google Login Demo</h2>
      {!user ? (
        <GoogleLoginButton onLogin={handleLogin} />
      ) : (
        <>
          <p>Welcome, {user.name} ({user.email})</p>
          <button onClick={handleCheck}>Check /api/me</button>
        </>
      )}
    </div>
  );
}

export default App;