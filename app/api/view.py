from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()


@router.get("/dashboard-view", response_class=HTMLResponse)
def dashboard_view():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Game Dashboard</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                padding: 20px;
                background: #111;
                color: white;
            }
            .card {
                background: #222;
                padding: 15px;
                margin: 10px 0;
                border-radius: 10px;
            }
            .btn {
                padding: 10px 15px;
                margin: 5px;
                cursor: pointer;
                border: none;
                border-radius: 5px;
                font-weight: bold;
            }
            .study { background: #3498db; color: white; }
            .workout { background: #e74c3c; color: white; }
            .meditation { background: #2ecc71; color: white; }
            .login-btn { background: #9b59b6; color: white; }
            .logout-btn { background: #555; color: white; }
            .progress-bar {
                background: #444;
                border-radius: 10px;
                overflow: hidden;
                margin-top: 10px;
            }
            .progress {
                background: #f1c40f;
                height: 20px;
            }
            input {
                padding: 10px;
                border-radius: 6px;
                border: none;
                width: 240px;
                margin-right: 10px;
            }
            #app {
                display: none;
            }
        </style>
    </head>
    <body>
        <h1>🎮 Game Dashboard</h1>

        <div id="loginSection" class="card">
            <h3>Login / Create User</h3>
            <input type="text" id="usernameInput" placeholder="Kullanıcı adı gir">
            <button class="btn login-btn" onclick="login()">Giriş Yap</button>
            <p id="loginMessage"></p>
        </div>

        <div id="app">
            <div id="profile" class="card"></div>
            <div id="stats" class="card"></div>
            <div id="quests" class="card"></div>

            <div class="card">
                <h3>Actions</h3>
                <button class="btn study" onclick="sendAction('study')">Study +1</button>
                <button class="btn workout" onclick="sendAction('workout')">Workout +1</button>
                <button class="btn meditation" onclick="sendAction('meditation')">Meditation +1</button>
                <button class="btn logout-btn" onclick="logout()">Çıkış Yap</button>
            </div>
        </div>

        <script>
            let userId = localStorage.getItem("user_id");
            let username = localStorage.getItem("username");

            async function login() {
                const usernameInput = document.getElementById("usernameInput").value.trim();

                if (!usernameInput) {
                    document.getElementById("loginMessage").innerText = "Kullanıcı adı boş olamaz";
                    return;
                }

                const res = await fetch("/auth/login", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ username: usernameInput })
                });

                const data = await res.json();

                if (data.error) {
                    document.getElementById("loginMessage").innerText = data.error;
                    return;
                }

                localStorage.setItem("user_id", data.user_id);
                localStorage.setItem("username", data.username);

                userId = data.user_id;
                username = data.username;

                document.getElementById("loginMessage").innerText = "Giriş başarılı";
                showApp();
                loadDashboard();
            }

            function logout() {
                localStorage.removeItem("user_id");
                localStorage.removeItem("username");
                userId = null;
                username = null;
                document.getElementById("app").style.display = "none";
                document.getElementById("loginSection").style.display = "block";
            }

            function showApp() {
                document.getElementById("loginSection").style.display = "none";
                document.getElementById("app").style.display = "block";
            }

            async function loadDashboard() {
                if (!userId) return;

                const res = await fetch(`/users/${userId}/dashboard`);
                const data = await res.json();

                document.getElementById("profile").innerHTML = `
                    <h3>${data.profile.username}</h3>
                    Level: ${data.profile.level} | XP: ${data.profile.xp} | Streak: ${data.profile.streak}
                    <div class="progress-bar">
                        <div class="progress" style="width:${data.profile.level_progress.progress_percent}%"></div>
                    </div>
                    %${data.profile.level_progress.progress_percent} - Next: ${data.profile.level_progress.xp_to_next_level} XP
                `;

                document.getElementById("stats").innerHTML = `
                    <h3>Stats</h3>
                    Strength: ${data.stats.strength} <br>
                    Discipline: ${data.stats.discipline} <br>
                    Focus: ${data.stats.focus} <br>
                    Energy: ${data.stats.energy}
                `;

                document.getElementById("quests").innerHTML = `
                    <h3>Daily Quests</h3>
                    ${data.today_quests.map(q => `
                        <div>
                            ${q.title} (${q.progress_value}/${q.target_value}) ${q.is_completed ? "✅" : ""}
                        </div>
                    `).join("")}
                `;
            }

            async function sendAction(type) {
                if (!userId) return;

                await fetch("/actions/log", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({
                        user_id: Number(userId),
                        action_type: type,
                        value: 1
                    })
                });

                loadDashboard();
            }

            if (userId && username) {
                showApp();
                loadDashboard();
            }
        </script>
    </body>
    </html>
    """