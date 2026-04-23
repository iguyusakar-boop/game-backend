import { useState } from "react";

function App() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const handleLogin = async () => {
    try {
      const response = await fetch("https://web-production-6df2f.up.railway.app/auth/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
        body: new URLSearchParams({
          username: username,
          password: password,
        }),
      });

      const data = await response.json();
      console.log(data);

      alert("Giriş başarılı!");
    } catch (error) {
      console.error(error);
      alert("Hata oluştu");
    }
  };

  return (
    <div style={{ padding: "40px", fontFamily: "Arial" }}>
      <h1>🔥 Game App</h1>

      <div style={{ marginTop: "20px" }}>
        <input
          placeholder="Kullanıcı adı"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
      </div>

      <div style={{ marginTop: "10px" }}>
        <input
          type="password"
          placeholder="Şifre"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
      </div>

      <button style={{ marginTop: "20px" }} onClick={handleLogin}>
        Giriş Yap
      </button>
    </div>
  );
}

export default App;