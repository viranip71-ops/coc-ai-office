import streamlit as st
import json
import urllib.request
import urllib.parse

st.set_page_config(
    page_title="CoC AI Multi-Agent Office HQ",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="collapsed"
)

PLAYER_TAG = "#GVQPR9J82"
API_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjkzZDNkZTk3LTJmZmYtNDM5YS05NTgzLTM3NzZkMGZhMzc3NSIsImlhdCI6MTc4ODA3NDY5Niwic3ViIjoiZGV2ZWxvcGVyLzllYmFiYzlmLTM0M2UtNDU2My1iYmM0LTAyOGJjZWE1MTEzMyIsInNjb3BlcyI6WyJjbGFzaCJdLCJsaW1pdHMiOlt7InRpZXIiOiJkZXZlbG9wZXIvc2lsdmVyIiwidHlwZSI6InRocm90dGxpbmcifSx7ImNpZHJzIjpbIjM0LjkuMTQ0LjIyMCJdLCJ0eXBlIjoiY2xpZW50In1dfQ.C-AuXUoXnCJA6pazFYpYg0IUgivSctttnT7iJEZPyiAQj8tAlJ940xrbxTWQlU53EcROBzbOu8vpqDVpO_fvvA"

@st.cache_data(ttl=300)
def get_server_ip():
    try:
        return urllib.request.urlopen('https://api.ipify.org').read().decode('utf8')
    except:
        return "Unknown"

server_ip = get_server_ip()

def fetch_supercell_data():
    try:
        clean = urllib.parse.quote(PLAYER_TAG.strip())
        url = f"https://api.clashofclans.com/v1/players/{clean}"
        req = urllib.request.Request(url, headers={"Authorization": f"Bearer {API_TOKEN.strip()}", "Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            return json.loads(resp.read().decode('utf-8')), True
    except Exception as e:
        return None, False

live_api, is_live = fetch_supercell_data()

if is_live and live_api:
    p_name = live_api.get('name', 'Chief')
    th_lvl = live_api.get('townHallLevel', 14)
    trophies = live_api.get('trophies', 3200)
    clan_name = live_api.get('clan', {}).get('name', 'Active Clan')
    bh_lvl = live_api.get('builderHallLevel', 9)
    status_tag = f"🟢 LIVE SYNC: {p_name} (TH{th_lvl})"
else:
    p_name = "Chief"
    th_lvl = 14
    trophies = 3200
    clan_name = "Active Clan"
    bh_lvl = 9
    status_tag = f"🟡 STREAMLIT IP: {server_ip}"

app_html = f"""
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; font-family: monospace; }}
  body {{ background: #030712; color: #f9fafb; padding: 4px; overflow-x: hidden; }}

  .top-banner {{
    background: #111827;
    border: 1px solid #374151;
    border-radius: 8px;
    padding: 8px 12px;
    margin-bottom: 8px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 11px;
  }}

  .main-wrapper {{
    display: flex;
    flex-direction: column;
    gap: 8px;
    max-width: 900px;
    margin: auto;
  }}

  .canvas-card {{
    background: #0f172a;
    border: 2px solid #1e293b;
    border-radius: 12px;
    padding: 8px;
  }}

  canvas {{
    background: #020617;
    border: 2px solid #334155;
    border-radius: 8px;
    width: 100%;
    height: auto;
    display: block;
    image-rendering: pixelated;
  }}

  .chat-card {{
    background: #0b0f19;
    border: 2px solid #1e293b;
    border-radius: 12px;
    overflow: hidden;
    display: flex;
    flex-direction: column;
    height: 380px;
  }}

  .terminal-header {{
    background: #1e293b;
    padding: 8px 12px;
    font-size: 12px;
    font-weight: bold;
    color: #facc15;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }}

  .chat-log {{
    flex: 1;
    padding: 10px;
    overflow-y: auto;
    font-size: 12px;
    line-height: 1.4;
    background: #030712;
  }}

  .msg {{ margin-bottom: 8px; padding: 6px 10px; border-radius: 6px; font-size: 12px; }}
  .msg-user {{ background: #1e3a8a; color: #93c5fd; margin-left: 20%; text-align: right; }}
  .msg-ceo {{ background: #1f2937; color: #f9fafb; border-left: 4px solid #facc15; }}
  .msg-manager {{ background: #064e3b; color: #a7f3d0; border-left: 4px solid #10b981; }}

  .quick-bar {{
    display: flex;
    gap: 6px;
    padding: 6px 8px;
    background: #111827;
    overflow-x: auto;
    border-top: 1px solid #1e293b;
  }}

  .btn-cmd {{
    background: #1f2937;
    color: #e5e7eb;
    border: 1px solid #374151;
    padding: 6px 10px;
    font-size: 11px;
    border-radius: 6px;
    cursor: pointer;
    white-space: nowrap;
  }}

  .input-bar {{
    display: flex;
    padding: 8px;
    background: #0f172a;
    border-top: 1px solid #1e293b;
  }}

  .input-bar input {{
    flex: 1;
    background: #1e293b;
    border: 1px solid #374151;
    color: #fff;
    padding: 7px 10px;
    border-radius: 6px;
    font-size: 12px;
    outline: none;
  }}

  .input-bar button {{
    margin-left: 6px;
    background: #f59e0b;
    color: #000;
    font-weight: bold;
    border: none;
    padding: 7px 14px;
    border-radius: 6px;
    cursor: pointer;
  }}
</style>
</head>
<body>

<div class="main-wrapper">

  <div class="top-banner">
    <span style="font-weight:bold; color:#38bdf8;">🏢 CLASH AI HQ (VIRTUAL OFFICE)</span>
    <span style="color:#34d399;">{status_tag}</span>
  </div>

  <div class="canvas-card">
    <canvas id="officeCanvas" width="560" height="360"></canvas>
  </div>

  <div class="chat-card">
    <div class="terminal-header">
      <span>👑 CEO EXECUTIVE TERMINAL</span>
      <span style="background: #22c55e; width: 8px; height: 8px; border-radius: 50%; display: inline-block;"></span>
    </div>
    
    <div class="chat-log" id="chatLog">
      <div class="msg msg-ceo">
        <b>👑 Central CEO:</b> Chief <b>{p_name}</b>, બધી જ ૪ કેબિન્સમાં મેનેજર્સ હાજર છે. નીચેથી કોઈપણ ડિપાર્ટમેન્ટનો રિપોર્ટ મંગાવો અથવા સીધો કમાન્ડ આપો.
      </div>
    </div>

    <div class="quick-bar">
      <button class="btn-cmd" onclick="requestReport('hv')">🏰 Home Village</button>
      <button class="btn-cmd" onclick="requestReport('bb')">🌙 Builder Base</button>
      <button class="btn-cmd" onclick="requestReport('clan')">🛡️ Clan War</button>
      <button class="btn-cmd" onclick="requestReport('cap')">🏛️ Clan Capital</button>
      <button class="btn-cmd" onclick="requestReport('all')">⭐ CEO 360° Audit</button>
    </div>

    <div class="input-bar">
      <input type="text" id="userInp" placeholder="CEO ને સવાલ પૂછો..." onkeydown="if(event.key==='Enter') sendCustomMsg()">
      <button onclick="sendCustomMsg()">Send</button>
    </div>
  </div>

</div>

<script>
const canvas = document.getElementById("officeCanvas");
const ctx = canvas.getContext("2d");

const chiefData = {{
  name: "{p_name}",
  th: {th_lvl},
  trophies: {trophies},
  clan: "{clan_name}",
  bh: {bh_lvl}
}};

const rooms = {{
  ceo:  {{ x: 190, y: 15,  w: 180, h: 100, title: "👑 CEO CABIN", color: "#1e1b4b", border: "#facc15" }},
  hv:   {{ x: 20,  y: 135, w: 220, h: 95,  title: "🏰 HOME VILLAGE DEPT", color: "#0c4a6e", border: "#38bdf8" }},
  bb:   {{ x: 320, y: 135, w: 220, h: 95,  title: "🌙 BUILDER BASE LAB", color: "#3b0764", border: "#c084fc" }},
  clan: {{ x: 20,  y: 245, w: 220, h: 100, title: "🛡️ WAR ROOM", color: "#064e3b", border: "#4ade80" }},
  cap:  {{ x: 320, y: 245, w: 220, h: 100, title: "🏛️ CAPITAL TREASURY", color: "#7c2d12", border: "#fb923c" }}
}};

const agents = {{
  hv:   {{ name: "HV Manager", origX: 70, origY: 175, x: 70, y: 175, color: "#0284c7", skin: "#fed7aa", hair: "#78350f", targetX: 250, targetY: 90, state: "idle" }},
  bb:   {{ name: "BB Specialist", origX: 370, origY: 175, x: 370, y: 175, color: "#9333ea", skin: "#fed7aa", hair: "#facc15", targetX: 300, targetY: 90, state: "idle" }},
  clan: {{ name: "War General", origX: 70, origY: 285, x: 70, y: 285, color: "#16a34a", skin: "#fed7aa", hair: "#1e293b", targetX: 250, targetY: 100, state: "idle" }},
  cap:  {{ name: "Capital Banker", origX: 370, origY: 285, x: 370, y: 285, color: "#ea580c", skin: "#fed7aa", hair: "#b91c1c", targetX: 300, targetY: 100, state: "idle" }}
}};

function drawHuman(x, y, skin, shirt, hair, isCEO=false) {{
  ctx.fillStyle = "rgba(0,0,0,0.3)";
  ctx.beginPath(); ctx.ellipse(x, y+14, 9, 4, 0, 0, Math.PI*2); ctx.fill();

  ctx.fillStyle = shirt;
  ctx.fillRect(x-6, y+2, 12, 10);

  if (isCEO) {{
    ctx.fillStyle = "#ef4444";
    ctx.fillRect(x-1, y+3, 2, 7);
  }}

  ctx.fillStyle = skin;
  ctx.beginPath(); ctx.arc(x, y-2, 6, 0, Math.PI*2); ctx.fill();

  ctx.fillStyle = hair;
  ctx.beginPath(); ctx.arc(x, y-5, 6, Math.PI, Math.PI*2); ctx.fill();
}}

function drawDesk(x, y, w, h, woodColor, monitorSide="center") {{
  ctx.fillStyle = woodColor;
  ctx.fillRect(x, y, w, h);
  ctx.strokeStyle = "rgba(255,255,255,0.15)";
  ctx.strokeRect(x, y, w, h);

  let mx = monitorSide === "left" ? x+6 : (monitorSide === "right" ? x+w-18 : x+w/2-6);
  ctx.fillStyle = "#0f172a";
  ctx.fillRect(mx, y+2, 12, 8);
  ctx.fillStyle = "#38bdf8";
  ctx.fillRect(mx+1, y+3, 10, 6);
}}

function drawOffice() {{
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  ctx.fillStyle = "#090d16"; ctx.fillRect(0, 0, canvas.width, canvas.height);

  ctx.strokeStyle = "#1e293b"; ctx.lineWidth = 1;
  for (let i=0; i<canvas.width; i+=25) {{ ctx.beginPath(); ctx.moveTo(i,0); ctx.lineTo(i,canvas.height); ctx.stroke(); }}

  for (let r in rooms) {{
    let rm = rooms[r];
    ctx.fillStyle = rm.color;
    ctx.fillRect(rm.x, rm.y, rm.w, rm.h);
    ctx.strokeStyle = rm.border;
    ctx.lineWidth = 2;
    ctx.strokeRect(rm.x, rm.y, rm.w, rm.h);

    ctx.fillStyle = rm.border;
    ctx.font = "bold 9px monospace";
    ctx.fillText(rm.title, rm.x + 8, rm.y + 14);
  }}

  drawDesk(240, 45, 80, 36, "#78350f");
  drawHuman(280, 36, "#fed7aa", "#1e293b", "#e2e8f0", true);
  ctx.fillStyle = "#facc15";
  ctx.font = "bold 9px monospace";
  ctx.fillText("👑 CEO", 265, 70);

  drawDesk(100, 160, 50, 30, "#334155", "right");
  drawDesk(400, 160, 50, 30, "#334155", "left");
  drawDesk(100, 270, 50, 30, "#334155", "right");
  drawDesk(400, 270, 50, 30, "#334155", "left");

  for (let k in agents) {{
    let ag = agents[k];
    drawHuman(ag.x, ag.y, ag.skin, ag.color, ag.hair);
    
    ctx.fillStyle = "#cbd5e1";
    ctx.font = "8px monospace";
    ctx.fillText(ag.name, ag.x - 18, ag.y + 24);

    if (ag.state === "walking_to_ceo") {{
      drawBubble(ag.x, ag.y - 14, "🚶 Reporting...");
    }} else if (ag.state === "at_ceo") {{
      drawBubble(ag.x, ag.y - 14, "📋 File Submitted!");
    }}
  }}

  requestAnimationFrame(drawOffice);
}}

function drawBubble(x, y, txt) {{
  ctx.fillStyle = "#0f172a";
  ctx.fillRect(x - 35, y - 10, 70, 13);
  ctx.strokeStyle = "#facc15";
  ctx.strokeRect(x - 35, y - 10, 70, 13);
  ctx.fillStyle = "#f8fafc";
  ctx.font = "8px monospace";
  ctx.fillText(txt, x - 30, y);
}}

function moveAgentToCEO(key, onArrive) {{
  let ag = agents[key];
  ag.state = "walking_to_ceo";
  let step = setInterval(() => {{
    let dx = ag.targetX - ag.x, dy = ag.targetY - ag.y;
    let dist = Math.sqrt(dx*dx + dy*dy);
    if (dist > 3) {{
      ag.x += (dx/dist)*3; ag.y += (dy/dist)*3;
    }} else {{
      ag.x = ag.targetX; ag.y = ag.targetY;
      ag.state = "at_ceo";
      clearInterval(step);
      setTimeout(() => {{
        walkBack(ag, onArrive);
      }}, 1000);
    }}
  }}, 25);
}}

function walkBack(ag, callback) {{
  let step = setInterval(() => {{
    let dx = ag.origX - ag.x, dy = ag.origY - ag.y;
    let dist = Math.sqrt(dx*dx + dy*dy);
    if (dist > 3) {{
      ag.x += (dx/dist)*3; ag.y += (dy/dist)*3;
    }} else {{
      ag.x = ag.origX; ag.y = ag.origY;
      ag.state = "idle";
      clearInterval(step);
      if (callback) callback();
    }}
  }}, 25);
}}

function logMsg(sender, text, type) {{
  let log = document.getElementById("chatLog");
  let d = document.createElement("div");
  d.className = `msg msg-${{type}}`;
  d.innerHTML = `<b>${{sender}}:</b> ${{text}}`;
  log.appendChild(d);
  log.scrollTop = log.scrollHeight;
}}

function requestReport(dept) {{
  if (dept === 'hv') {{
    logMsg("Chief", "Home Village નો રિપોર્ટ આપો.", "user");
    logMsg("👑 CEO", "Home Village Manager ને કેબિનમાં બોલાવ્યો છે...", "ceo");
    moveAgentToCEO('hv', () => {{
      logMsg("🏰 HV Manager", `<b>Town Hall ${{chiefData.th}} Live Report:</b><br>• Trophies: ${{chiefData.trophies}} 🏆<br>• Builders: 5 Busy, 1 Available soon<br>• Focus: Heroes & Core Defences`, "manager");
      logMsg("👑 CEO", "રિપોર્ટ મંજૂર છે. બિલ્ડર ફ્રી થતાં જ હીરો અપગ્રેડ શરૂ કરો.", "ceo");
    }});
  }}
  else if (dept === 'bb') {{
    logMsg("Chief", "Builder Base રિપોર્ટ આપો.", "user");
    logMsg("👑 CEO", "Builder Base Specialist આવી રહ્યો છે...", "ceo");
    moveAgentToCEO('bb', () => {{
      logMsg("🌙 BB Specialist", `<b>Builder Base ${{chiefData.bh}} Report:</b><br>• 6th Builder (B.O.B): Active<br>• Priority: Battle Copter & Troops Maxing`, "manager");
      logMsg("👑 CEO", "બેટલ કોપ્ટર અપગ્રેડ ચાલુ રાખો.", "ceo");
    }});
  }}
  else if (dept === 'clan') {{
    logMsg("Chief", "Clan War અને CWL રિપોર્ટ આપો.", "user");
    logMsg("👑 CEO", "War General ને ફાઇલ સાથે બોલાવ્યો છે...", "ceo");
    moveAgentToCEO('clan', () => {{
      logMsg("🛡️ War General", `<b>Clan: ${{chiefData.clan}}</b><br>• War Tracking: Active<br>• CWL Bonus Candidate: ${{chiefData.name}} (#GVQPR9J82)`, "manager");
      logMsg("👑 CEO", "સારો પરફોર્મન્સ છે. બોનસ મેડલ્સ સુરક્ષિત રહેશે.", "ceo");
    }});
  }}
  else if (dept === 'cap') {{
    logMsg("Chief", "Clan Capital Raid રિપોર્ટ આપો.", "user");
    logMsg("👑 CEO", "Capital Banker રિપોર્ટ લઈને આવી રહ્યો છે...", "ceo");
    moveAgentToCEO('cap', () => {{
      logMsg("🏛️ Capital Banker", "<b>Clan Capital Brief:</b><br>• 6/6 Raid Attacks Used<br>• Capital Gold Donated to District Hall", "manager");
      logMsg("👑 CEO", "રેઇડ વિકેન્ડ પૂર્ણ થયું છે.", "ceo");
    }});
  }}
  else if (dept === 'all') {{
    logMsg("Chief", "આજનો ઓલ-ઓવર 360° રિપોર્ટ આપો.", "user");
    logMsg("👑 CEO", "<b>⭐ 360° EXECUTIVE AUDIT:</b><br>🔴 <b>Urgent:</b> ૧ બિલ્ડર ટૂંક સમયમાં ફ્રી થશે.<br>🟠 <b>High:</b> Heroes Upgrades Schedule કરો.<br>🟢 <b>Done:</b> Clan Raids & War Attacks પૂર્ણ.", "ceo");
  }}
}}

function sendCustomMsg() {{
  let inp = document.getElementById("userInp");
  let val = inp.value.trim();
  if (!val) return;
  logMsg("Chief", val, "user");
  inp.value = "";
  let l = val.toLowerCase();
  if (l.includes("home") || l.includes("hero") || l.includes("th")) requestReport('hv');
  else if (l.includes("builder") || l.includes("bb")) requestReport('bb');
  else if (l.includes("clan") || l.includes("war")) requestReport('clan');
  else if (l.includes("capital") || l.includes("raid")) requestReport('cap');
  else logMsg("👑 CEO", `ટાસ્ક નોંધાઈ ગયો છે: "${{val}}". હું સંબંધિત મેનેજરને સૂચના આપી દઉં છું.`, "ceo");
}}

drawOffice();
</script>
</body>
</html>
"""

st.components.v1.html(app_html, height=820, scrolling=False)
