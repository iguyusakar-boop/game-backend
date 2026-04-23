import { useEffect, useState } from "react";

const API_BASE = "https://web-production-6df2f.up.railway.app";

function App() {
  const [page, setPage] = useState("login");
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(false);
  const [lastActionResult, setLastActionResult] = useState(null);
  const [notice, setNotice] = useState("");

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) return;

    const fetchMe = async () => {
      try {
        setLoading(true);
        const response = await fetch(`${API_BASE}/auth/me`, {
          headers: { Authorization: `Bearer ${token}` },
        });
        const data = await response.json();
        if (!response.ok) {
          localStorage.removeItem("token");
          setPage("login");
          return;
        }
        setUser(data);
        setPage("dashboard");
      } catch (error) {
        localStorage.removeItem("token");
        setPage("login");
      } finally {
        setLoading(false);
      }
    };

    fetchMe();
  }, []);

  const fetchCurrentUser = async (token) => {
    const response = await fetch(`${API_BASE}/auth/me`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    const data = await response.json();
    if (!response.ok) throw new Error("Kullanıcı bilgisi alınamadı");
    setUser(data);
  };

  const handleLogin = async () => {
    try {
      setLoading(true);
      setNotice("");
      const response = await fetch(`${API_BASE}/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: new URLSearchParams({ username, password }),
      });
      const data = await response.json();
      if (!response.ok) {
        setNotice(data.detail || "Giriş başarısız");
        return;
      }
      localStorage.setItem("token", data.access_token);
      await fetchCurrentUser(data.access_token);
      setPage("dashboard");
    } catch (error) {
      setNotice("Giriş sırasında hata oluştu");
    } finally {
      setLoading(false);
    }
  };

  const handleAction = async () => {
    try {
      setLoading(true);
      setNotice("");
      const token = localStorage.getItem("token");
      const response = await fetch(`${API_BASE}/action?action_type=study&value=1`, {
        method: "POST",
        headers: { Authorization: `Bearer ${token}` },
      });
      const data = await response.json();
      if (!response.ok) {
        setNotice(data.detail || "Action gönderilemedi");
        return;
      }
      setLastActionResult(data);
      const meResponse = await fetch(`${API_BASE}/auth/me`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      const meData = await meResponse.json();
      if (meResponse.ok) setUser(meData);
      setNotice(`XP kazandın! +${data.xp_gained} XP`);
    } catch (error) {
      setNotice("Action sırasında hata oluştu");
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem("token");
    setUser(null);
    setLastActionResult(null);
    setUsername("");
    setPassword("");
    setNotice("");
    setPage("login");
  };

  const xpCurrent = user ? user.xp % 100 : 0;

  if (loading) {
    return (
      <div style={{
        minHeight: "100vh", backgroundColor: "#0b1020", color: "white",
        display: "flex", justifyContent: "center", alignItems: "center",
        fontFamily: "Arial", fontSize: "24px",
      }}>
        Yükleniyor...
      </div>
    );
  }

  if (page === "dashboard" && user) {
    return (
      <div style={{
        minHeight: "100vh", backgroundColor: "#0b1020", color: "white",
        fontFamily: "Arial", padding: "32px",
      }}>
        <div style={{ maxWidth: "980px", margin: "0 auto" }}>

          <h1 style={{ fontSize: "56px", marginBottom: "4px" }}>🎮 Dashboard</h1>
          <p style={{ color: "#b7c2d0", marginTop: 0 }}>Oyuncu panelin hazır.</p>

          {notice && (
            <div style={{
              marginBottom: "20px", padding: "14px 16px",
              backgroundColor: "#16213a", border: "1px solid #2b3b63",
              borderRadius: "12px",
            }}>
              {notice}
            </div>
          )}

          {/* Profil + Hızlı Bakış */}
          <div style={{ display: "grid", gridTemplateColumns: "2fr 1fr", gap: "20px" }}>
            <div style={{
              backgroundColor: "#121a30", border: "1px solid #24304d",
              borderRadius: "16px", padding: "24px",
            }}>
              <h2 style={{ marginTop: 0 }}>Profil</h2>
              <p><strong>ID:</strong> {user.id}</p>
              <p><strong>Kullanıcı Adı:</strong> {user.username}</p>
              <p><strong>Toplam XP:</strong> {user.xp}</p>
              <p><strong>Level:</strong> {user.level}</p>
              <p><strong>Streak:</strong> {user.streak}</p>

              <div style={{ marginTop: "20px", marginBottom: "8px" }}>
                Level Progress: {xpCurrent}/100 XP
              </div>
              <div style={{
                width: "100%", height: "18px", backgroundColor: "#0b1020",
                borderRadius: "999px", overflow: "hidden", border: "1px solid #2a3655",
              }}>
                <div style={{
                  width: `${xpCurrent}%`, height: "100%", backgroundColor: "#4ade80",
                  transition: "width 0.4s",
                }} />
              </div>

              <div style={{ marginTop: "24px", display: "flex", gap: "12px" }}>
                <button onClick={handleAction} style={{
                  padding: "12px 18px", fontSize: "16px", cursor: "pointer",
                  borderRadius: "10px", border: "none", backgroundColor: "#6c63ff",
                  color: "white",
                }}>
                  Study Action (+XP)
                </button>
                <button onClick={handleLogout} style={{
                  padding: "12px 18px", fontSize: "16px", cursor: "pointer",
                  borderRadius: "10px", border: "none", backgroundColor: "#2a2a3d",
                  color: "white",
                }}>
                  Çıkış Yap
                </button>
              </div>
            </div>

            <div style={{
              backgroundColor: "#121a30", border: "1px solid #24304d",
              borderRadius: "16px", padding: "24px",
            }}>
              <h2 style={{ marginTop: 0 }}>Hızlı Bakış</h2>
              <p>Bugünkü hedef: 1 action tamamla</p>
              <p>Durum: Oyuncu aktif</p>
              <p>Son durum: {lastActionResult ? "Action işlendi" : "Henüz action yok"}</p>
            </div>
          </div>

          {/* Statslar */}
          {lastActionResult && (
            <>
              <div style={{
                display: "grid", gridTemplateColumns: "repeat(4, 1fr)",
                gap: "16px", marginTop: "20px",
              }}>
                {[
                  { label: "Discipline", value: lastActionResult.stats?.discipline ?? 0 },
                  { label: "Focus",      value: lastActionResult.stats?.focus ?? 0 },
                  { label: "Strength",   value: lastActionResult.stats?.strength ?? 0 },
                  { label: "Energy",     value: lastActionResult.stats?.energy ?? 0 },
                ].map((stat) => (
                  <div key={stat.label} style={{
                    backgroundColor: "#121a30", border: "1px solid #24304d",
                    borderRadius: "16px", padding: "20px",
                  }}>
                    <h3 style={{ marginTop: 0 }}>{stat.label}</h3>
                    <div style={{ fontSize: "28px", fontWeight: "bold" }}>{stat.value}</div>
                  </div>
                ))}
              </div>

              {/* Questler */}
              <div style={{
                marginTop: "20px", backgroundColor: "#121a30",
                border: "1px solid #24304d", borderRadius: "16px", padding: "24px",
              }}>
                <h2 style={{ marginTop: 0 }}>Questler</h2>

                {lastActionResult.quests?.length > 0 ? (
                  <div style={{ display: "grid", gap: "12px" }}>
                    {lastActionResult.quests.map((quest) => (
                      <div key={quest.id} style={{
                        padding: "16px",
                        backgroundColor: quest.completed ? "#0d2218" : "#0f1728",
                        border: `1px solid ${quest.completed ? "#4ade80" : "#253252"}`,
                        borderRadius: "12px",
                      }}>
                        {/* Başlık + rozet */}
                        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "8px" }}>
                          <div style={{ fontWeight: "bold", fontSize: "15px" }}>
                            {quest.completed ? "✅ " : "🔲 "}{quest.title}
                          </div>
                          <div style={{
                            fontSize: "12px", padding: "3px 10px", borderRadius: "999px",
                            backgroundColor: quest.completed ? "#14532d" : "#1e2a45",
                            color: quest.completed ? "#4ade80" : "#93c5fd",
                          }}>
                            {quest.completed ? "Tamamlandı" : "Devam ediyor"}
                          </div>
                        </div>

                        {/* Progress bar */}
                        <div style={{ fontSize: "13px", color: "#aaa", marginBottom: "6px" }}>
                          İlerleme: {quest.progress} / {quest.target_value}
                        </div>
                        <div style={{
                          backgroundColor: "#1a2235", borderRadius: "4px",
                          height: "8px", overflow: "hidden",
                        }}>
                          <div style={{
                            width: `${Math.min((quest.progress / quest.target_value) * 100, 100)}%`,
                            height: "100%",
                            backgroundColor: quest.completed ? "#4ade80" : "#6c63ff",
                            borderRadius: "4px",
                            transition: "width 0.4s",
                          }} />
                        </div>

                        <div style={{ fontSize: "12px", color: "#888", marginTop: "8px" }}>
                          Ödül: +{quest.xp_reward} XP
                        </div>
                      </div>
                    ))}
                  </div>
                ) : (
                  <p style={{ color: "#888" }}>Henüz quest verisi yok.</p>
                )}
              </div>
            </>
          )}

        </div>
      </div>
    );
  }

  // Login ekranı
  return (
    <div style={{
      minHeight: "100vh", backgroundColor: "#0b1020",
      display: "flex", justifyContent: "center", alignItems: "center",
      color: "white", fontFamily: "Arial",
    }}>
      <div style={{ textAlign: "center", width: "320px" }}>
        <h1 style={{ fontSize: "64px", marginBottom: "24px" }}>🔥 Game App</h1>

        {notice && (
          <div style={{
            marginBottom: "16px", padding: "12px 14px", backgroundColor: "#16213a",
            border: "1px solid #2b3b63", borderRadius: "12px", textAlign: "left",
          }}>
            {notice}
          </div>
        )}

        <div style={{ display: "flex", flexDirection: "column", gap: "14px" }}>
          <input
            type="text" placeholder="Kullanıcı adı" value={username}
            onChange={(e) => setUsername(e.target.value)}
            style={{ padding: "12px", fontSize: "16px", borderRadius: "10px", border: "none" }}
          />
          <input
            type="password" placeholder="Şifre" value={password}
            onChange={(e) => setPassword(e.target.value)}
            style={{ padding: "12px", fontSize: "16px", borderRadius: "10px", border: "none" }}
          />
          <button onClick={handleLogin} style={{
            padding: "12px", fontSize: "18px", cursor: "pointer",
            borderRadius: "10px", border: "none", backgroundColor: "#6c63ff", color: "white",
          }}>
            Giriş Yap
          </button>
        </div>
      </div>
    </div>
  );
}

export default App;