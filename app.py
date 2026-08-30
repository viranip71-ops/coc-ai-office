import streamlit as st
import json
import urllib.request
import urllib.parse

st.set_page_config(
    page_title="CoC HQ - Multi-Agent Office",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="collapsed"
)

PLAYER_TAG = "#GVQPR9J82"
API_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjkzZDNkZTk3LTJmZmYtNDM5YS05NTgzLTM3NzZkMGZhMzc3NSIsImlhdCI6MTc4ODA3NDY5Niwic3ViIjoiZGV2ZWxvcGVyLzllYmFiYzlmLTM0M2UtNDU2My1iYmM0LTAyOGJjZWE1MTEzMyIsInNjb3BlcyI6WyJjbGFzaCJdLCJsaW1pdHMiOlt7InRpZXIiOiJkZXZlbG9wZXIvc2lsdmVyIiwidHlwZSI6InRocm90dGxpbmcifSx7ImNpZHJzIjpbIjM0LjkuMTQ0LjIyMCJdLCJ0eXBlIjoiY2xpZW50In1dfQ.C-AuXUoXnCJA6pazFYpYg0IUgivSctttnT7iJEZPyiAQj8tAlJ940xrbxTWQlU53EcROBzbOu8vpqDVpO_fvvA"

@st.cache_data(ttl=300)
def get_ip():
    try:
        return urllib.request.urlopen('https://api.ipify.org').read().decode('utf8')
    except:
        return "Unknown"

server_ip = get_ip()

def fetch_data():
    try:
        clean = urllib.parse.quote(PLAYER_TAG.strip())
        url = f"https://api.clashofclans.com/v1/players/{clean}"
        req = urllib.request.Request(url, headers={"Authorization": f"Bearer {API_TOKEN.strip()}", "Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            return json.loads(resp.read().decode('utf-8')), True
    except:
        return None, False

live_api, is_live = fetch_data()

if is_live and live_api:
    p_name = live_api.get('name', 'Chief')
    th_lvl = live_api.get('townHallLevel', 14)
    trophies = live_api.get('trophies', 3200)
    clan_name = live_api.get('clan', {}).get('name', 'Indian Warriors')
    clan_tag = live_api.get('clan', {}).get('tag', '#CLAN')
    war_stars = live_api.get('warStars', 450)
    bh_lvl = live_api.get('builderHallLevel', 9)
    cap_gold = live_api.get('clanCapitalContributions', 150000)
    
    heroes_arr = [f"{h['name']} Lvl {h['level']}/{h['maxLevel']}" for h in live_api.get('heroes', []) if h.get('village') == 'home']
    heroes_str = ", ".join(heroes_arr) if heroes_arr else "Barbarian King Lvl 75, Archer Queen Lvl 80, Grand Warden Lvl 55"
    status_label = f"🟢 LIVE SYNC ACTIVE: {p_name} (TH{th_lvl})"
else:
    p_name = "Chief Virani"
    th_lvl = 15
    trophies = 3450
    clan_name = "Royal Elite Clan"
    clan_tag = "#2YQL89CV"
    war_stars = 720
    bh_lvl = 9
    cap_gold = 385000
    heroes_str = "Barbarian King Lvl 82/90, Archer Queen Lvl 85/90, Grand Warden Lvl 60/65, Royal Champion Lvl 32/40"
    status_label = f"🟡 STREAMLIT IP: {server_ip} (Add to Supercell Key for Real-Time Sync)"

app_html = f"""
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, monospace; }}
  body {{ background: #030712; color: #f9fafb; padding: 4px; }}
  
  .wrapper {{ max-width: 950px; margin: auto; display: flex; flex-direction: column; gap: 8px; }}
  
  .banner {{
    background: #0f172a;
    border: 1px solid #1e293b;
    border-radius: 8px;
    padding: 8px 12px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 11px;
  }}

  .canvas-box {{
    background: #090d16;
    border: 2px solid #1e293b;
    border-radius: 12px;
    padding: 6px;
  }}

  canvas {{
    background: #0f172a;
    border: 1px solid #334155;
    border-radius: 8px;
    width: 100%;
    display: block;
  }}

  .chat-box {{
    background: #0b0f19;
    border: 2px solid #1e293b;
    border-radius: 12px;
    height: 420px;
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }}

  .chat-head {{
    background: #1e293b;
    padding: 8px 12px;
    font-size: 12px;
    font-weight: bold;
    color: #facc15;
    display: flex;
    justify-content: space-between;
  }}

  .chat-log {{
    flex: 1;
    padding: 10px;
    overflow-y: auto;
    font-size: 12px;
    line-height: 1.5;
    background: #030712;
  }}

  .msg {{ margin-bottom: 10px; padding: 8px 12px; border-radius: 8px; font-size: 12px; }}
  .msg-user {{ background: #1e3a8a; color: #bfdbfe; margin-left: 15%; text-align: right; }}
  .msg-ceo {{ background: #1e293b; color: #f8fafc; border-left: 4px solid #facc15; }}
  .msg-mgr {{ background: #064e3b; color: #a7f3d0; border-left: 4px solid #10b981; }}

  .quick-cmds {{
    display: flex;
    gap: 6px;
    padding: 6px 8px;
    background: #0f172a;
    overflow-x: auto;
    border-top: 1px solid #1e293b;
  }}

  .btn-cmd {{
    background: #1e293b;
    color: #e2e8f0;
    border: 1px solid #334155;
    padding: 6px 10px;
    font-size: 11px;
    border-radius: 6px;
    cursor: pointer;
    white-space: nowrap;
    font-weight: 500;
  }}
  .btn-cmd:hover {{ background: #334155; color: #38bdf8; }}

  .input-pane {{
    display: flex;
    padding: 8px;
    background: #0f172a;
    border-top: 1px solid #1e293b;
  }}

  .input-pane input {{
    flex: 1;
    background: #1e293b;
    border: 1px solid #334155;
    color: #fff;
    padding: 8px 12px;
    border-radius: 6px;
    font-size: 12px;
    outline: none;
  }}

  .input-pane button {{
    margin-left: 6px;
    background: #f59e0b;
    color: #000;
    font-weight: bold;
    border: none;
    padding: 8px 16px;
    border-radius: 6px;
    cursor: pointer;
  }}
</style>
</head>
<body>

<div class="wrapper">
  
  <div class="banner">
    <span style="font-weight:bold; color:#38bdf8;">🏢 CLASH OF CLANS AI HEADQUARTERS</span>
    <span style="color:#34d399;">{status_label}</span>
  </div>

  <!-- 2D Top-Down Office Canvas -->
  <div class="canvas-box">
    <canvas id="officeCanvas" width="600" height="380"></canvas>
  </div>

  <!-- Terminal Chat -->
  <div class="chat-box">
    <div class="chat-head">
      <span>👑 CEO EXECUTIVE TERMINAL & LIVE CHAT</span>
      <span style="color: #4ade80;">● ACTIVE</span>
    </div>
    
    <div class="chat-log" id="chatLog">
      <div class="msg msg-ceo">
        <b>👑 Central CEO:</b> Greetings Chief <b>{p_name}</b>! તમામ ૪ મેનેજરો પોતાની ઓફિસ કેબિનમાં હાજર છે. જ્યારે તમે રિપોર્ટ માંગશો ત્યારે પટાવાળો (Peon) મેનેજર પાસેથી ફાઈલ લાવીને મારા ટેબલ પર જમા કરશે.
      </div>
    </div>

    <div class="quick-cmds">
      <button class="btn-cmd" onclick="triggerReport('war')">🛡️ Clan War Report</button>
      <button class="btn-cmd" onclick="triggerReport('hv')">🏰 Village & Hero Audit</button>
      <button class="btn-cmd" onclick="triggerReport('bb')">🌙 Builder Base Plan</button>
      <button class="btn-cmd" onclick="triggerReport('cap')">🏛️ Clan Capital Loot</button>
      <button class="btn-cmd" onclick="triggerReport('all')">⭐ 360° Executive Brief</button>
    </div>

    <div class="input-pane">
      <input type="text" id="userInput" placeholder="CEO ને સવાલ પૂછો (દા.ત. War status, Hero upgrade, base defence...)" onkeydown="if(event.key==='Enter') handleUserSend()">
      <button onclick="handleUserSend()">Send</button>
    </div>
  </div>

</div>

<script>
const canvas = document.getElementById("officeCanvas");
const ctx = canvas.getContext("2d");

// Live Data Object
const profile = {{
  name: "{p_name}",
  th: {th_lvl},
  trophies: {trophies},
  clan: "{clan_name}",
  tag: "{clan_tag}",
  warStars: {war_stars},
  bh: {bh_lvl},
  heroes: "{heroes_str}",
  capitalGold: "{cap_gold}"
}};

// Office Rooms Layout
const rooms = [
  {{ id: "ceo",  x: 210, y: 15,  w: 180, h: 100, title: "👑 CEO CABIN", color: "#1e1b4b", border: "#facc15", door: {{x: 300, y: 115}} }},
  {{ id: "hv",   x: 20,  y: 145, w: 220, h: 100, title: "🏰 HOME VILLAGE DEPT", color: "#0c4a6e", border: "#38bdf8", door: {{x: 240, y: 190}} }},
  {{ id: "bb",   x: 360, y: 145, w: 220, h: 100, title: "🌙 BUILDER BASE LAB", color: "#3b0764", border: "#c084fc", door: {{x: 360, y: 190}} }},
  {{ id: "clan", x: 20,  y: 265, w: 220, h: 100, title: "🛡️ WAR ROOM & CWL", color: "#064e3b", border: "#4ade80", door: {{x: 240, y: 310}} }},
  {{ id: "cap",  x: 360, y: 265, w: 220, h: 100, title: "🏛️ CAPITAL TREASURY", color: "#7c2d12", border: "#fb923c", door: {{x: 360, y: 310}} }}
];

// Characters
const characters = {{
  ceo: {{ x: 300, y: 55, skin: "#fed7aa", suit: "#0f172a", hair: "#e2e8f0", sitting: true }},
  hv: {{ x: 80, y: 190, skin: "#fed7aa", suit: "#0284c7", hair: "#78350f", name: "HV Manager", room: "hv" }},
  bb: {{ x: 420, y: 190, skin: "#fed7aa", suit: "#9333ea", hair: "#facc15", name: "BB Specialist", room: "bb" }},
  clan: {{ x: 80, y: 310, skin: "#fed7aa", suit: "#16a34a", hair: "#1e293b", name: "War General", room: "clan" }},
  cap: {{ x: 420, y: 310, skin: "#fed7aa", suit: "#ea580c", hair: "#b91c1c", name: "Capital Banker", room: "cap" }},
  peon: {{ x: 300, y: 220, origX: 300, origY: 220, skin: "#fbcfe8", suit: "#64748b", cap: "#dc2626", state: "idle", targetX: 300, targetY: 220, hasFile: false }}
}};

function drawPlant(x, y) {{
  ctx.fillStyle = "#15803d";
  ctx.beginPath(); ctx.arc(x, y, 7, 0, Math.PI*2); ctx.fill();
  ctx.fillStyle = "#86efac";
  ctx.beginPath(); ctx.arc(x-2, y-2, 4, 0, Math.PI*2); ctx.fill();
}}

function drawOffice() {{
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  // Corridor Flooring Tiles
  ctx.fillStyle = "#090d16";
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  ctx.strokeStyle = "#1e293b";
  ctx.lineWidth = 1;
  for(let i=0; i<canvas.width; i+=20) {{ ctx.beginPath(); ctx.moveTo(i,0); ctx.lineTo(i,canvas.height); ctx.stroke(); }}

  // Draw 5 Department Rooms
  rooms.forEach(rm => {{
    ctx.fillStyle = rm.color;
    ctx.fillRect(rm.x, rm.y, rm.w, rm.h);
    ctx.strokeStyle = rm.border;
    ctx.lineWidth = 2;
    ctx.strokeRect(rm.x, rm.y, rm.w, rm.h);

    // Door Gap
    ctx.strokeStyle = "#090d16";
    ctx.lineWidth = 3;
    if(rm.door.y === 115) {{
      ctx.beginPath(); ctx.moveTo(rm.door.x - 15, rm.door.y); ctx.lineTo(rm.door.x + 15, rm.door.y); ctx.stroke();
    }} else {{
      ctx.beginPath(); ctx.moveTo(rm.door.x, rm.door.y - 12); ctx.lineTo(rm.door.x, rm.door.y + 12); ctx.stroke();
    }}

    // Title Tag
    ctx.fillStyle = rm.border;
    ctx.font = "bold 9px monospace";
    ctx.fillText(rm.title, rm.x + 8, rm.y + 14);
  }});

  // Plants & Water Cooler
  drawPlant(195, 135);
  drawPlant(400, 135);
  ctx.fillStyle = "#38bdf8"; ctx.fillRect(290, 140, 14, 20); // Water Cooler

  // Desks & Chairs
  drawDesk(260, 65, 80, 30, "#78350f", "center"); // CEO Desk
  drawDesk(110, 175, 50, 26, "#334155", "right");
  drawDesk(450, 175, 50, 26, "#334155", "left");
  drawDesk(110, 295, 50, 26, "#334155", "right");
  drawDesk(450, 295, 50, 26, "#334155", "left");

  // Peon Waiting Station
  ctx.fillStyle = "#1e293b"; ctx.fillRect(285, 205, 30, 20);
  ctx.fillStyle = "#94a3b8"; ctx.font = "7px monospace"; ctx.fillText("RUNNER", 286, 235);

  // Draw Managers & CEO
  drawPerson(characters.ceo.x, characters.ceo.y, characters.ceo.skin, characters.ceo.suit, characters.ceo.hair, true);
  drawPerson(characters.hv.x, characters.hv.y, characters.hv.skin, characters.hv.suit, characters.hv.hair);
  drawPerson(characters.bb.x, characters.bb.y, characters.bb.skin, characters.bb.suit, characters.bb.hair);
  drawPerson(characters.clan.x, characters.clan.y, characters.clan.skin, characters.clan.suit, characters.clan.hair);
  drawPerson(characters.cap.x, characters.cap.y, characters.cap.skin, characters.cap.suit, characters.cap.hair);

  // Draw Peon (Runner)
  let p = characters.peon;
  drawPerson(p.x, p.y, p.skin, p.suit, p.cap, false, p.hasFile);

  if(p.state === "to_mgr") drawSpeech(p.x, p.y - 14, "🏃 Picking File...");
  else if(p.state === "to_ceo") drawSpeech(p.x, p.y - 14, "📁 Delivering to CEO...");
  else if(p.state === "at_ceo") drawSpeech(p.x, p.y - 14, "👑 File Submitted!");

  requestAnimationFrame(drawOffice);
}}

function drawDesk(x, y, w, h, color, pcPos) {{
  ctx.fillStyle = color;
  ctx.fillRect(x, y, w, h);
  ctx.strokeStyle = "rgba(255,255,255,0.15)";
  ctx.strokeRect(x, y, w, h);

  // Glowing PC Screen
  let mx = pcPos === "left" ? x+5 : (pcPos === "right" ? x+w-16 : x+w/2-6);
  ctx.fillStyle = "#0f172a"; ctx.fillRect(mx, y+3, 12, 8);
  ctx.fillStyle = "#38bdf8"; ctx.fillRect(mx+1, y+4, 10, 6);
}}

function drawPerson(x, y, skin, suit, hair, isCEO=false, hasFile=false) {{
  // Shadow
  ctx.fillStyle = "rgba(0,0,0,0.35)";
  ctx.beginPath(); ctx.ellipse(x, y+10, 8, 4, 0, 0, Math.PI*2); ctx.fill();

  // Shirt / Body
  ctx.fillStyle = suit;
  ctx.fillRect(x-6, y, 12, 10);

  // Tie
  if(isCEO) {{ ctx.fillStyle = "#ef4444"; ctx.fillRect(x-1, y+1, 2, 7); }}

  // Head
  ctx.fillStyle = skin;
  ctx.beginPath(); ctx.arc(x, y-4, 5, 0, Math.PI*2); ctx.fill();

  // Hair / Cap
  ctx.fillStyle = hair;
  ctx.beginPath(); ctx.arc(x, y-6, 5, Math.PI, Math.PI*2); ctx.fill();

  // File folder in hand
  if(hasFile) {{
    ctx.fillStyle = "#facc15";
    ctx.fillRect(x+5, y+2, 7, 9);
    ctx.strokeStyle = "#fff";
    ctx.strokeRect(x+5, y+2, 7, 9);
  }}
}}

function drawSpeech(x, y, txt) {{
  ctx.fillStyle = "#0f172a";
  ctx.fillRect(x - 45, y - 10, 90, 14);
  ctx.strokeStyle = "#facc15";
  ctx.strokeRect(x - 45, y - 10, 90, 14);
  ctx.fillStyle = "#f8fafc";
  ctx.font = "8px monospace";
  ctx.fillText(txt, x - 40, y);
}}

// Peon Walking Pipeline: Lobby -> Manager Room -> CEO Cabin -> Lobby
function dispatchPeon(deptId, callback) {{
  let p = characters.peon;
  let mgr = characters[deptId];
  let rm = rooms.find(r => r.id === deptId);

  // Step 1: Walk to Manager
  p.state = "to_mgr";
  walkTo(mgr.x + 18, mgr.y, () => {{
    p.hasFile = true; // Collect file
    p.state = "to_ceo";

    // Step 2: Walk to CEO Desk
    walkTo(300, 100, () => {{
      p.state = "at_ceo";
      p.hasFile = false; // Hand over file

      setTimeout(() => {{
        // Step 3: Walk back to lobby
        p.state = "idle";
        walkTo(p.origX, p.origY, callback);
      }}, 800);
    }});
  }});
}}

function walkTo(tx, ty, onDone) {{
  let p = characters.peon;
  let speed = 4;
  let timer = setInterval(() => {{
    let dx = tx - p.x, dy = ty - p.y;
    let dist = Math.sqrt(dx*dx + dy*dy);
    if(dist > speed) {{
      p.x += (dx/dist)*speed;
      p.y += (dy/dist)*speed;
    }} else {{
      p.x = tx; p.y = ty;
      clearInterval(timer);
      if(onDone) onDone();
    }}
  }}, 25);
}}

function logMsg(sender, text, type) {{
  let box = document.getElementById("chatLog");
  let d = document.createElement("div");
  d.className = `msg msg-${{type}}`;
  d.innerHTML = `<b>${{sender}}:</b> ${{text}}`;
  box.appendChild(d);
  box.scrollTop = box.scrollHeight;
}}

function triggerReport(type) {{
  if(type === 'war') {{
    logMsg("Chief", "Clan War નો સંપુર્ણ એનાલિસિસ રિપોર્ટ આપો.", "user");
    logMsg("👑 CEO", "પટાવાળાને War Room માંથી લાઈવ વોર ફાઈલ લાવવા મોકલ્યો છે...", "ceo");
    dispatchPeon('clan', () => {{
      let warHTML = `
      <b>⚔️ CLAN WAR & CWL DEEP AUDIT REPORT:</b><br>
      • <b>Clan:</b> ${{profile.clan}} (${{profile.tag}})<br>
      • <b>War Status:</b> 45 vs 41 Stars (Lead by +4 ⭐)<br>
      • <b>Attacks Used:</b> Clan 28/30 Attacks (93.3% Participation)<br>
      • <b>3-Star Conversion Rate:</b> 78.5% (11 Triple Attacks)<br>
      • <b>Win Probability:</b> 🟢 <b>92% High Chance of Victory</b><br>
      • <b>Top Performers:</b> 1. ${{profile.name}} (6⭐ 200%), 2. ShadowKing (6⭐ 194%)<br>
      • <b>Remaining Targets:</b> Enemy #4 & #7 still have 2 stars open.
      `;
      logMsg("🛡️ War General", warHTML, "mgr");
      logMsg("👑 CEO", "વોરમાં આપણી સ્થિતિ મજબૂત છે. CWL બોનસ માટે ${{profile.name}} નું નામ નોમિનેટ કર્યું છે.", "ceo");
    }});
  }}
  else if(type === 'hv') {{
    logMsg("Chief", "Home Village અને Heroes નો સ્ટેટસ રિપોર્ટ આપો.", "user");
    logMsg("👑 CEO", "પટાવાળો Home Village મેનેજર પાસેથી ફાઈલ લાવી રહ્યો છે...", "ceo");
    dispatchPeon('hv', () => {{
      let hvHTML = `
      <b>🏰 HOME VILLAGE & HERO PROGRESSION REPORT:</b><br>
      • <b>Town Hall:</b> Level ${{profile.th}} | <b>Trophies:</b> ${{profile.trophies}} 🏆<br>
      • <b>Heroes Status:</b> ${{profile.heroes}}<br>
      • <b>Builders Status:</b> 5 Busy (1 Builder free in ~2.5 hours)<br>
      • <b>Next Priority Upgrades:</b><br>
        1. Monolith (Lvl 2) - Core Defence<br>
        2. Archer Queen - Max Level Push<br>
        3. Giant Gauntlet / Frozen Arrow Equipment Sync
      `;
      logMsg("🏰 HV Manager", hvHTML, "mgr");
      logMsg("👑 CEO", "બિલ્ડર ફ્રી થતાં જ મોનોલિથ અપગ્રેડ કરવા ઓર્ડર આપ્યો છે.", "ceo");
    }});
  }}
  else if(type === 'bb') {{
    logMsg("Chief", "Builder Base રિપોર્ટ આપો.", "user");
    dispatchPeon('bb', () => {{
      let bbHTML = `
      <b>🌙 BUILDER BASE 2.0 AUDIT:</b><br>
      • <b>Builder Hall:</b> Level ${{profile.bh}}<br>
      • <b>6th Builder Status:</b> 🟢 <b>B.O.B Unlocked & Fully Active</b><br>
      • <b>Recommendation:</b> Battle Copter Level 25 અપગ્રેડ કરો.
      `;
      logMsg("🌙 BB Specialist", bbHTML, "mgr");
      logMsg("👑 CEO", "બિલ્ડર બેઝ લાઈવ ટ્રેકિંગ સક્રિય છે.", "ceo");
    }});
  }}
  else if(type === 'cap') {{
    logMsg("Chief", "Clan Capital Raid રિપોર્ટ આપો.", "user");
    dispatchPeon('cap', () => {{
      let capHTML = `
      <b>🏛️ CLAN CAPITAL RAID RESULTS:</b><br>
      • <b>Total Capital Gold Looted/Contributed:</b> ${{profile.capitalGold}} 🪙<br>
      • <b>Personal Attacks:</b> 6/6 Attacks Completed (Max Efficiency)<br>
      • <b>Average Gold Per Attack:</b> ~4,350 Gold<br>
      • <b>Treasury Recommendation:</b> District Hall 5 અપગ્રેડમાં ફાળવો.
      `;
      logMsg("🏛️ Capital Banker", capHTML, "mgr");
      logMsg("👑 CEO", "રેઇડ મેડલ્સ આ સોમવારે ક્રેડિટ થઈ જશે.", "ceo");
    }});
  }}
  else if(type === 'all') {{
    logMsg("Chief", "આજનો ઓલ-ઓવર 360° એક્ઝિક્યુટિવ રિપોર્ટ આપો.", "user");
    logMsg("👑 CEO", "<b>⭐ 360° EXECUTIVE AUDIT:</b><br>🔴 <b>Urgent:</b> ૧ બિલ્ડર ટૂંક સમયમાં ફ્રી થશે (ગોલ્ડ સ્ટોરેજ ભરી રાખો).<br>🟠 <b>War:</b> ક્લેન વોરમાં ૯૨% વિનિંગ ચાન્સ છે.<br>🟢 <b>Capital:</b> તમામ ૬ રેઇડ અટેક્સ પૂર્ણ થયેલા છે.", "ceo");
  }}
}}

function handleUserSend() {{
  let inp = document.getElementById("userInput");
  let val = inp.value.trim();
  if(!val) return;
  logMsg("Chief", val, "user");
  inp.value = "";
  let l = val.toLowerCase();
  if(l.includes("war") || l.includes("cwl") || l.includes("clan")) triggerReport('war');
  else if(l.includes("hero") || l.includes("home") || l.includes("upgrade") || l.includes("th")) triggerReport('hv');
  else if(l.includes("builder") || l.includes("bb") || l.includes("night")) triggerReport('bb');
  else if(l.includes("capital") || l.includes("raid") || l.includes("gold")) triggerReport('cap');
  else {{
    logMsg("👑 CEO", `Chief, તમારો સંદેશ મળ્યો: "${{val}}". હું પટાવાળા દ્વારા આ ટાસ્ક સંબંધિત મેનેજર સુધી પહોંચાડી રહ્યો છું.`, "ceo");
  }}
}}

drawOffice();
</script>
</body>
</html>
"""

st.components.v1.html(app_html, height=850, scrolling=False)
