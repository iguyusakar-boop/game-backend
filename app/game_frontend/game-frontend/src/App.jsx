import { useEffect, useState } from "react";

const API_BASE = "http://127.0.0.1:8000";

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
        if (!response.ok) { localStorage.removeItem("token"); setPage("login"); return; }
        setUser(data);
        setPage("dashboard");
      } catch { localStorage.removeItem("token"); setPage("login"); }
      finally { setLoading(false); }
    };
    fetchMe();
  }, []);

  const fetchCurrentUser = async (token) => {
    const res = await fetch(`${API_BASE}/auth/me`, { headers: { Authorization: `Bearer ${token}` } });
    const data = await res.json();
    if (!res.ok) throw new Error("Kullanıcı bilgisi alınamadı");
    setUser(data);
  };

  const handleLogin = async () => {
    try {
      setLoading(true); setNotice("");
      const res = await fetch(`${API_BASE}/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: new URLSearchParams({ username, password }),
      });
      const data = await res.json();
      if (!res.ok) { setNotice(data.detail || "Giriş başarısız"); return; }
      localStorage.setItem("token", data.access_token);
      await fetchCurrentUser(data.access_token);
      setPage("dashboard");
    } catch { setNotice("Giriş sırasında hata oluştu"); }
    finally { setLoading(false); }
  };

  const handleRegister = async () => {
    try {
      setLoading(true); setNotice("");
      const res = await fetch(`${API_BASE}/auth/register`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password }),
      });
      const data = await res.json();
      if (!res.ok) { setNotice(data.detail || "Kayıt başarısız"); return; }
      setNotice("Kayıt başarılı! Giriş yapabilirsin.");
      setPage("login");
    } catch { setNotice("Kayıt sırasında hata oluştu"); }
    finally { setLoading(false); }
  };

  const handleAction = async (actionType) => {
    try {
      setLoading(true); setNotice("");
      const token = localStorage.getItem("token");
      const res = await fetch(`${API_BASE}/action?action_type=${actionType}&value=1`, {
        method: "POST",
        headers: { Authorization: `Bearer ${token}` },
      });
      const data = await res.json();
      if (!res.ok) { setNotice(data.detail || "Action gönderilemedi"); return; }
      setLastActionResult(data);
      const meRes = await fetch(`${API_BASE}/auth/me`, { headers: { Authorization: `Bearer ${token}` } });
      const meData = await meRes.json();
      if (meRes.ok) setUser(meData);
      setNotice(`XP kazandın! +${data.xp_gained} XP`);
    } catch { setNotice("Action sırasında hata oluştu"); }
    finally { setLoading(false); }
  };

  const handleLogout = () => {
    localStorage.removeItem("token");
    setUser(null); setLastActionResult(null);
    setUsername(""); setPassword(""); setNotice("");
    setPage("login");
  };

  const xpCurrent = user ? user.xp % 100 : 0;

  // Avatar — stat seviyesine göre emoji ve renk
  const getAvatar = (stats) => {
    if (!stats) return { emoji: "🧍", color: "#888", title: "Başlangıç" };
    const total = (stats.discipline || 0) + (stats.focus || 0) + (stats.strength || 0) + (stats.energy || 0);
    if (total >= 40) return { emoji: "🦸", color: "#f59e0b", title: "Efsane" };
    if (total >= 20) return { emoji: "⚔️", color: "#6c63ff", title: "Savaşçı" };
    if (total >= 10) return { emoji: "🧗", color: "#4ade80", title: "Gelişen" };
    return { emoji: "🧍", color: "#888", title: "Başlangıç" };
  };

  const avatar = getAvatar(lastActionResult?.stats);

  const ACTION_BUTTONS = [
    { type: "study",  label: "📚 Study",  color: "#6c63ff", desc: "+Disiplin +Odak" },
    { type: "work",   label: "💼 Work",   color: "#f59e0b", desc: "+Güç" },
    { type: "health", label: "🏃 Health", color: "#4ade80", desc: "+Enerji" },
  ];

  if (loading) return (
    <div style={{ minHeight: "100vh", backgroundColor: "#0b1020", color: "white", display: "flex", justifyContent: "center", alignItems: "center", fontFamily: "Arial", fontSize: "24px" }}>
      Yükleniyor...
    </div>
  );

  if (page === "dashboard" && user) return (
    <div style={{ minHeight: "100vh", backgroundColor: "#0b1020", color: "white", fontFamily: "Arial", padding: "32px" }}>
      <div style={{ maxWidth: "980px", margin: "0 auto" }}>

        <h1 style={{ fontSize: "48px", marginBottom: "4px" }}>🎮 Dashboard</h1>
        <p style={{ color: "#b7c2d0", marginTop: 0 }}>Oyuncu panelin hazır.</p>

        {notice && (
          <div style={{ marginBottom: "20px", padding: "14px 16px", backgroundColor: "#16213a", border: "1px solid #2b3b63", borderRadius: "12px" }}>
            {notice}
          </div>
        )}

        <div style={{ display: "grid", gridTemplateColumns: "2fr 1fr", gap: "20px" }}>

          {/* Profil */}
          <div style={{ backgroundColor: "#121a30", border: "1px solid #24304d", borderRadius: "16px", padding: "24px" }}>

            {/* Avatar */}
            <div style={{ textAlign: "center", marginBottom: "16px" }}>
              <div style={{ fontSize: "64px", lineHeight: 1 }}>{avatar.emoji}</div>
              <div style={{ color: avatar.color, fontWeight: "bold", marginTop: "6px" }}>{avatar.title}</div>
            </div>

            <h2 style={{ marginTop: 0 }}>Profil</h2>
            <p><strong>Kullanıcı Adı:</strong> {user.username}</p>
            <p><strong>Toplam XP:</strong> {user.xp}</p>
            <p><strong>Level:</strong> {user.level}</p>
            <p><strong>Streak:</strong> {user.streak} 🔥</p>

            <div style={{ marginTop: "16px", marginBottom: "8px" }}>Level Progress: {xpCurrent}/100 XP</div>
            <div style={{ width: "100%", height: "18px", backgroundColor: "#0b1020", borderRadius: "999px", overflow: "hidden", border: "1px solid #2a3655" }}>
              <div style={{ width: `${xpCurrent}%`, height: "100%", backgroundColor: "#4ade80", transition: "width 0.4s" }} />
            </div>

            {/* Action butonları */}
            <div style={{ marginTop: "24px", display: "flex", gap: "10px", flexWrap: "wrap" }}>
              {ACTION_BUTTONS.map((btn) => (
                <button key={btn.type} onClick={() => handleAction(btn.type)} style={{
                  padding: "10px 16px", fontSize: "14px", cursor: "pointer",
                  borderRadius: "10px", border: "none",
                  backgroundColor: btn.color, color: btn.type === "health" ? "#000" : "white",
                  fontWeight: "bold",
                }}>
                  {btn.label}
                  <div style={{ fontSize: "11px", opacity: 0.8, fontWeight: "normal" }}>{btn.desc}</div>
                </button>
              ))}
              <button onClick={handleLogout} style={{ padding: "10px 16px", fontSize: "14px", cursor: "pointer", borderRadius: "10px", border: "none", backgroundColor: "#2a2a3d", color: "white" }}>
                Çıkış
              </button>
            </div>
          </div>

          {/* Hızlı Bakış */}
          <div style={{ backgroundColor: "#121a30", border: "1px solid #24304d", borderRadius: "16px", padding: "24px" }}>
            <h2 style={{ marginTop: 0 }}>Hızlı Bakış</h2>
            <p>📚 Study → Disiplin + Odak</p>
            <p>💼 Work → Güç</p>
            <p>🏃 Health → Enerji</p>
            <hr style={{ borderColor: "#24304d" }} />
            <p>Son durum: {lastActionResult ? "Action işlendi ✅" : "Henüz action yok"}</p>
          </div>
        </div>

        {/* Statlar */}
        {lastActionResult && (
          <>
            <div style={{ display: "grid", gridTemplateColumns: "repeat(4, 1fr)", gap: "16px", marginTop: "20px" }}>
              {[
                { label: "Discipline", value: lastActionResult.stats?.discipline ?? 0, color: "#6c63ff" },
                { label: "Focus",      value: lastActionResult.stats?.focus ?? 0,      color: "#38bdf8" },
                { label: "Strength",   value: lastActionResult.stats?.strength ?? 0,   color: "#f59e0b" },
                { label: "Energy",     value: lastActionResult.stats?.energy ?? 0,     color: "#4ade80" },
              ].map((stat) => (
                <div key={stat.label} style={{ backgroundColor: "#121a30", border: `1px solid ${stat.color}44`, borderRadius: "16px", padding: "20px", textAlign: "center" }}>
                  <h3 style={{ marginTop: 0, color: stat.color }}>{stat.label}</h3>
                  <div style={{ fontSize: "32px", fontWeight: "bold" }}>{stat.value}</div>
                </div>
              ))}
            </div>

            {/* Questler */}
            <div style={{ marginTop: "20px", backgroundColor: "#121a30", border: "1px solid #24304d", borderRadius: "16px", padding: "24px" }}>
              <h2 style={{ marginTop: 0 }}>Questler</h2>
              {lastActionResult.quests?.length > 0 ? (
                <div style={{ display: "grid", gap: "12px" }}>
                  {lastActionResult.quests.map((quest) => (
                    <div key={quest.id} style={{ padding: "16px", backgroundColor: quest.completed ? "#0d2218" : "#0f1728", border: `1px solid ${quest.completed ? "#4ade80" : "#253252"}`, borderRadius: "12px" }}>
                      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "8px" }}>
                        <div style={{ fontWeight: "bold" }}>{quest.completed ? "✅ " : "🔲 "}{quest.title}</div>
                        <div style={{ fontSize: "12px", padding: "3px 10px", borderRadius: "999px", backgroundColor: quest.completed ? "#14532d" : "#1e2a45", color: quest.completed ? "#4ade80" : "#93c5fd" }}>
                          {quest.completed ? "Tamamlandı" : "Devam ediyor"}
                        </div>
                      </div>
                      <div style={{ fontSize: "13px", color: "#aaa", marginBottom: "6px" }}>İlerleme: {quest.progress} / {quest.target_value}</div>
                      <div style={{ backgroundColor: "#1a2235", borderRadius: "4px", height: "8px", overflow: "hidden" }}>
                        <div style={{ width: `${Math.min((quest.progress / quest.target_value) * 100, 100)}%`, height: "100%", backgroundColor: quest.completed ? "#4ade80" : "#6c63ff", borderRadius: "4px", transition: "width 0.4s" }} />
                      </div>
                      <div style={{ fontSize: "12px", color: "#888", marginTop: "8px" }}>Ödül: +{quest.xp_reward} XP</div>
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

  // Login / Register ekranı
  return (
    <div style={{ minHeight: "100vh", backgroundColor: "#0b1020", display: "flex", justifyContent: "center", alignItems: "center", color: "white", fontFamily: "Arial" }}>
      <div style={{ textAlign: "center", width: "340px" }}>
        <h1 style={{ fontSize: "56px", marginBottom: "8px" }}>🔥 Game App</h1>

        {/* Sekme */}
        <div style={{ display: "flex", marginBottom: "24px", borderRadius: "10px", overflow: "hidden", border: "1px solid #2b3b63" }}>
          <button onClick={() => { setPage("login"); setNotice(""); }} style={{ flex: 1, padding: "12px", fontSize: "15px", cursor: "pointer", border: "none", backgroundColor: page === "login" ? "#6c63ff" : "#16213a", color: "white", fontWeight: page === "login" ? "bold" : "normal" }}>
            Giriş Yap
          </button>
          <button onClick={() => { setPage("register"); setNotice(""); }} style={{ flex: 1, padding: "12px", fontSize: "15px", cursor: "pointer", border: "none", backgroundColor: page === "register" ? "#6c63ff" : "#16213a", color: "white", fontWeight: page === "register" ? "bold" : "normal" }}>
            Kayıt Ol
          </button>
        </div>

        {notice && (
          <div style={{ marginBottom: "16px", padding: "12px 14px", backgroundColor: "#16213a", border: "1px solid #2b3b63", borderRadius: "12px", textAlign: "left" }}>
            {notice}
          </div>
        )}

        <div style={{ display: "flex", flexDirection: "column", gap: "14px" }}>
          <input type="text" placeholder="Kullanıcı adı" value={username} onChange={(e) => setUsername(e.target.value)}
            style={{ padding: "12px", fontSize: "16px", borderRadius: "10px", border: "none", backgroundColor: "#16213a", color: "white" }} />
          <input type="password" placeholder="Şifre" value={password} onChange={(e) => setPassword(e.target.value)}
            style={{ padding: "12px", fontSize: "16px", borderRadius: "10px", border: "none", backgroundColor: "#16213a", color: "white" }} />
          <button onClick={page === "login" ? handleLogin : handleRegister} style={{ padding: "12px", fontSize: "18px", cursor: "pointer", borderRadius: "10px", border: "none", backgroundColor: "#6c63ff", color: "white", fontWeight: "bold" }}>
            {page === "login" ? "Giriş Yap" : "Kayıt Ol"}
          </button>
        </div>
      </div>
    </div>
  );
}

export default App;