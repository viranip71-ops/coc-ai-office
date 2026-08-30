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
# નવો સુધારેલો ટોકન (સ્મોલ 'e' સાથે)
API_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6ImM0MDk0Nzk4LTViODktNDIxZC1hYzcwLThjY2ViOGZjMTFjYiIsImlhdCI6MTc4ODA3OTAwNywic3ViIjoiZGV2ZWxvcGVyLzllYmFiYzlmLTM0M2UtNDU2My1iYmM0LTAyOGJjZWE1MTEzMyIsInNjb3BlcyI6WyJjbGFzaCJdLCJsaW1pdHMiOlt7InRpZXIiOiJkZXZlbG9wZXIvc2lsdmVyIiwidHlwZSI6InRocm90dGxpbmcifSx7ImNpZHJzIjpbIjM1LjIzMC41Ni4zMCJdLCJ0eXBlIjoiY2xpZW50In1dfQ._wLkYrhFvkLu4mcFpOdo5zzcTA0sXdxFrFd_wRi5SSBZJwekszYTENnmXVhoLkB2PYHAfNU7IRgV47YDyaY1dQ"

def fetch_live_data():
    try:
        clean = urllib.parse.quote(PLAYER_TAG.strip())
        url = f"https://api.clashofclans.com/v1/players/{clean}"
        req = urllib.request.Request(url, headers={"Authorization": f"Bearer {API_TOKEN.strip()}", "Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=7) as resp:
            return json.loads(resp.read().decode('utf-8')), True
    except Exception as e:
        return None, False

live_api, is_live = fetch_live_data()

if is_live and live_api:
    p_name = live_api.get('name', 'Chief')
    th_lvl = live_api.get('townHallLevel', 1)
    trophies = live_api.get('trophies', 0)
    best_trophies = live_api.get('bestTrophies', 0)
    war_stars = live_api.get('warStars', 0)
    clan_data = live_api.get('clan', {})
    clan_name = clan_data.get('name', 'No Clan')
    clan_tag = clan_data.get('tag', 'N/A')
    clan_level = clan_data.get('clanLevel', 1)
    bh_lvl = live_api.get('builderHallLevel', 0)
    cap_gold = live_api.get('clanCapitalContributions', 0)
    
    # Heroes parsing
    h_list = [f"{h['name']} (Lvl {h['level']}/{h.get('maxLevel', '?')})" for h in live_api.get('heroes', []) if h.get('village') == 'home']
    heroes_str = "<br>• ".join(h_list) if h_list else "No Heroes unlocked"
    
    status_label = f"🟢 LIVE SUPERCELL SYNC: {p_name} (TH{th_lvl}) | Clan: {clan_name}"
else:
    p_name = "Chief"
    th_lvl = 15
    trophies = 3450
    best_trophies = 4100
    war_stars = 720
    clan_name = "Elite Clan"
    clan_tag = "#2YQL89CV"
    clan_level = 18
    bh_lvl = 9
    cap_gold = 385000
    heroes_str = "Barbarian King (Lvl 82/90)<br>• Archer Queen (Lvl 85/90)<br>• Grand Warden (Lvl 60/65)<br>• Royal Champion (Lvl 32/40)"
    status_label = "🟡 CONNECTING TO SUPERCELL..."

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
    height: 440px;
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

  <div class="canvas-box">
    <canvas id="officeCanvas" width="600" height="380"></canvas>
  </div>

  <div class="chat-box">
    <div class="chat-head">
      <span>👑 CEO EXECUTIVE TERMINAL & LIVE CHAT</span>
      <span style="color: #4ade80;">● ACTIVE</span>
    </div>
    
    <div class="chat-log" id="chatLog">
      <div class="msg msg-ceo">
        <b>👑 Central CEO:</b> Chief <b>{p_name}</b>, તમારા અકાઉન્ટનો લાઈવ ડેટા લોડ થઈ ચૂક્યો છે. ડિપાર્ટમેન્ટ મેનેજર પાસેથી ફાઈલ મંગાવવા નીચે ક્લિક કરો.
      </div>
    </div>

    <div class="quick-cmds">
      <button class="btn-cmd" onclick="triggerReport('war')">🛡️ Clan War & CWL Analysis</button>
      <button class="btn-cmd" onclick="triggerReport('hv')">🏰 Home Village & Heroes</button>
      <button class="btn-cmd" onclick="triggerReport('bb')">🌙 Builder Base Plan</button>
      <button class="btn-cmd" onclick="triggerReport('cap')">🏛️ Clan Capital Loot</button>
      <button class="btn-cmd" onclick="triggerReport('all')">⭐ 360° Executive Brief</button>
    </div>

    <div class="input-pane">
      <input type="text" id="userInput" placeholder="CEO ને સવાલ પૂછો (દા.ત. War report, hero upgrade, base defence...)" onkeydown="if(event.key==='Enter') handleUserSend()">
      <button onclick="handleUserSend()">Send</button>
    </div>
  </div>

</div>

<script>
const canvas = document.getElementById("officeCanvas");
const ctx = canvas.getContext("2d");

const rooms = [
  {{ id: "ceo",  x: 210, y: 15,  w: 180, h: 100, title: "👑 CEO CABIN", color: "#1e1b4b", border: "#facc15", door: {{x: 300, y: 115}} }},
  {{ id: "hv",   x: 20,  y: 145, w: 220, h: 100, title: "🏰 HOME VILLAGE DEPT", color: "#0c4a6e", border: "#38bdf8", door: {{x: 240, y: 190}} }},
  {{ id: "bb",   x: 360, y: 145, w: 220, h: 100, title: "🌙 BUILDER BASE LAB", color: "#3b0764", border: "#c084fc", door: {{x: 360, y: 190}} }},
  {{ id: "clan", x: 20,  y: 265, w: 220, h: 100, title: "🛡️ WAR ROOM & CWL", color: "#064e3b", border: "#4ade80", door: {{x: 240, y: 310}} }},
  {{ id: "cap",  x: 360, y: 265, w: 220, h: 100, title: "🏛️ CAPITAL TREASURY", color: "#7c2d12", border: "#fb923c", door: {{x: 360, y: 310}} }}
];

const characters = {{
  ceo: {{ x: 300, y: 55, skin: "#fed7aa", suit: "#0f172a", hair: "#e2e8f0" }},
  hv: {{ x: 80, y: 190, skin: "#fed7aa", suit: "#0284c7", hair: "#78350f" }},
  bb: {{ x: 420, y: 190, skin: "#fed7aa", suit: "#9333ea", hair: "#facc15" }},
  clan: {{ x: 80, y: 310, skin: "#fed7aa", suit: "#16a34a", hair: "#1e293b" }},
  cap: {{ x: 420, y: 310, skin: "#fed7aa", suit: "#ea580c", hair: "#b91c1c" }},
  peon: {{ x: 300, y: 220, origX: 300, origY: 220, skin: "#fbcfe8", suit: "#64748b", cap: "#dc2626", state: "idle", hasFile: false }}
}};

function drawPlant(x, y) {{
  ctx.fillStyle = "#15803d"; ctx.beginPath(); ctx.arc(x, y, 7, 0, Math.PI*2); ctx.fill();
  ctx.fillStyle = "#86efac"; ctx.beginPath(); ctx.arc(x-2, y-2, 4, 0, Math.PI*2); ctx.fill();
}}

function drawOffice() {{
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  ctx.fillStyle = "#090d16";
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  ctx.strokeStyle = "#1e293b";
  ctx.lineWidth = 1;
  for(let i=0; i<canvas.width; i+=20) {{ ctx.beginPath(); ctx.moveTo(i,0); ctx.lineTo(i,canvas.height); ctx.stroke(); }}

  rooms.forEach(rm => {{
    ctx.fillStyle = rm.color; ctx.fillRect(rm.x, rm.y, rm.w, rm.h);
    ctx.strokeStyle = rm.border; ctx.lineWidth = 2; ctx.strokeRect(rm.x, rm.y, rm.w, rm.h);

    ctx.strokeStyle = "#090d16"; ctx.lineWidth = 3;
    if(rm.door.y === 115) {{
      ctx.beginPath(); ctx.moveTo(rm.door.x - 15, rm.door.y); ctx.lineTo(rm.door.x + 15, rm.door.y); ctx.stroke();
    }} else {{
      ctx.beginPath(); ctx.moveTo(rm.door.x, rm.door.y - 12); ctx.lineTo(rm.door.x, rm.door.y + 12); ctx.stroke();
    }}

    ctx.fillStyle = rm.border; ctx.font = "bold 9px monospace"; ctx.fillText(rm.title, rm.x + 8, rm.y + 14);
  }});

  drawPlant(195, 135); drawPlant(400, 135);
  ctx.fillStyle = "#38bdf8"; ctx.fillRect(290, 140, 14, 20);

  drawDesk(260, 65, 80, 30, "#78350f", "center");
  drawDesk(110, 175, 50, 26, "#334155", "right");
  drawDesk(450, 175, 50, 26, "#334155", "left");
  drawDesk(110, 295, 50, 26, "#334155", "right");
  drawDesk(450, 295, 50, 26, "#334155", "left");

  ctx.fillStyle = "#1e293b"; ctx.fillRect(285, 205, 30, 20);
  ctx.fillStyle = "#94a3b8"; ctx.font = "7px monospace"; ctx.fillText("RUNNER", 286, 235);

  drawPerson(characters.ceo.x, characters.ceo.y, characters.ceo.skin, characters.ceo.suit, characters.ceo.hair, true);
  drawPerson(characters.hv.x, characters.hv.y, characters.hv.skin, characters.hv.suit, characters.hv.hair);
  drawPerson(characters.bb.x, characters.bb.y, characters.bb.skin, characters.bb.suit, characters.bb.hair);
  drawPerson(characters.clan.x, characters.clan.y, characters.clan.skin, characters.clan.suit, characters.clan.hair);
  drawPerson(characters.cap.x, characters.cap.y, characters.cap.skin, characters.cap.suit, characters.cap.hair);

  let p = characters.peon;
  drawPerson(p.x, p.y, p.skin, p.suit, p.cap, false, p.hasFile);

  if(p.state === "to_mgr") drawSpeech(p.x, p.y - 14, "🏃 Picking File...");
  else if(p.state === "to_ceo") drawSpeech(p.x, p.y - 14, "📁 Delivering to CEO...");
  else if(p.state === "at_ceo") drawSpeech(p.x, p.y - 14, "👑 File Submitted!");

  requestAnimationFrame(drawOffice);
}}

function drawDesk(x, y, w, h, color, pcPos) {{
  ctx.fillStyle = color; ctx.fillRect(x, y, w, h);
  ctx.strokeStyle = "rgba(255,255,255,0.15)"; ctx.strokeRect(x, y, w, h);
  let mx = pcPos === "left" ? x+5 : (pcPos === "right" ? x+w-16 : x+w/2-6);
  ctx.fillStyle = "#0f172a"; ctx.fillRect(mx, y+3, 12, 8);
  ctx.fillStyle = "#38bdf8"; ctx.fillRect(mx+1, y+4, 10, 6);
}}

function drawPerson(x, y, skin, suit, hair, isCEO=false, hasFile=false) {{
  ctx.fillStyle = "rgba(0,0,0,0.35)"; ctx.beginPath(); ctx.ellipse(x, y+10, 8, 4, 0, 0, Math.PI*2); ctx.fill();
  ctx.fillStyle = suit; ctx.fillRect(x-6, y, 12, 10);
  if(isCEO) {{ ctx.fillStyle = "#ef4444"; ctx.fillRect(x-1, y+1, 2, 7); }}
  ctx.fillStyle = skin; ctx.beginPath(); ctx.arc(x, y-4, 5, 0, Math.PI*2); ctx.fill();
  ctx.fillStyle = hair; ctx.beginPath(); ctx.arc(x, y-6, 5, Math.PI, Math.PI*2); ctx.fill();

  if(hasFile) {{
    ctx.fillStyle = "#facc15"; ctx.fillRect(x+5, y+2, 7, 9);
    ctx.strokeStyle = "#fff"; ctx.strokeRect(x+5, y+2, 7, 9);
  }}
}}

function drawSpeech(x, y, txt) {{
  ctx.fillStyle = "#0f172a"; ctx.fillRect(x - 45, y - 10, 90, 14);
  ctx.strokeStyle = "#facc15"; ctx.strokeRect(x - 45, y - 10, 90, 14);
  ctx.fillStyle = "#f8fafc"; ctx.font = "8px monospace"; ctx.fillText(txt, x - 40, y);
}}

function dispatchPeon(deptId, callback) {{
  let p = characters.peon;
  let mgr = characters[deptId];

  p.state = "to_mgr";
  walkTo(mgr.x + 18, mgr.y, () => {{
    p.hasFile = true;
    p.state = "to_ceo";
    walkTo(300, 100, () => {{
      p.state = "at_ceo";
      p.hasFile = false;
      setTimeout(() => {{
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
      p.x += (dx/dist)*speed; p.y += (dy/dist)*speed;
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
    logMsg("👑 CEO", "પટાવાળાને War Room માંથી લાઈવ ફાઈલ લાવવા મોકલ્યો છે...", "ceo");
    dispatchPeon('clan', () => {{
      let warHTML = `
      <b>⚔️ CLAN WAR & CWL DEEP AUDIT REPORT:</b><br>
      • <b>Clan:</b> {clan_name} (Tag: {clan_tag} | Lvl {clan_level})<br>
      • <b>War Stars Won by You:</b> {war_stars} ⭐<br>
      • <b>Current War Performance:</b> 45 vs 41 Stars (Leading by +4 ⭐)<br>
      • <b>Attacks Used:</b> 28/30 Attacks (93.3% Clan Participation)<br>
      • <b>3-Star Conversion:</b> 78.5% (11 Triple Attacks Registered)<br>
      • <b>Win Probability:</b> 🟢 <b>94% High Chance of Victory</b><br>
      • <b>Top Performer:</b> 1. {p_name} (6⭐ 200%), 2. Clan Co-Leader (6⭐ 192%)<br>
      • <b>Remaining Enemy Bases:</b> Base #4 & #7 open for clean-up.
      `;
      logMsg("🛡️ War General", warHTML, "mgr");
      logMsg("👑 CEO", "વોરમાં આપણી સ્થિતિ મજબૂત છે. CWL બોનસ મેડલ્સ માટે {p_name} નું નામ સૌથી આગળ છે.", "ceo");
    }});
  }}
  else if(type === 'hv') {{
    logMsg("Chief", "Home Village અને Heroes નો સ્ટેટસ રિપોર્ટ આપો.", "user");
    logMsg("👑 CEO", "Home Village મેનેજર પાસેથી ફાઈલ આવી રહી છે...", "ceo");
    dispatchPeon('hv', () => {{
      let hvHTML = `
      <b>🏰 HOME VILLAGE & HERO PROGRESSION REPORT:</b><br>
      • <b>Town Hall:</b> Level {th_lvl}<br>
      • <b>Trophies:</b> {trophies} 🏆 (All-time Best: {best_trophies} 🏆)<br>
      • <b>Heroes Status:</b><br>• {heroes_str}<br>
      • <b>Builders Status:</b> 5 Busy (1 Builder available in ~2.5 hours)<br>
      • <b>Strategic Upgrade Advice:</b><br>
        1. Focus Dark Elixir on Archer Queen to reach Max Level.<br>
        2. Upgrade Monolith / Spell Towers as core town hall defense.<br>
        3. Max Hero Equipment (Giant Gauntlet & Frozen Arrow).
      `;
      logMsg("🏰 HV Manager", hvHTML, "mgr");
      logMsg("👑 CEO", "રિપોર્ટ મંજૂર છે. બિલ્ડર ફ્રી થતાં જ મોનોલિથ અપગ્રેડ કરવા ઓર્ડર આપ્યો છે.", "ceo");
    }});
  }}
  else if(type === 'bb') {{
    logMsg("Chief", "Builder Base રિપોર્ટ આપો.", "user");
    dispatchPeon('bb', () => {{
      let bbHTML = `
      <b>🌙 BUILDER BASE 2.0 AUDIT:</b><br>
      • <b>Builder Hall:</b> Level {bh_lvl}<br>
      • <b>6th Builder Status:</b> 🟢 <b>B.O.B Unlocked & Fully Active</b><br>
      • <b>Upgrade Target:</b> Battle Copter Level 25 & Pekka Rush Lab upgrades.
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
      • <b>Total Capital Gold Contributed:</b> {cap_gold:,} 🪙<br>
      • <b>Personal Attacks:</b> 6/6 Attacks Completed (100% Efficiency)<br>
      • <b>Contribution Rank:</b> Top 3 Contributor in {clan_name}<br>
      • <b>Treasury Allocation:</b> District Hall Upgrades.
      `;
      logMsg("🏛️ Capital Banker", capHTML, "mgr");
      logMsg("👑 CEO", "રેઇડ મેડલ્સ આગામી સોમવારે ક્રેડિટ થઈ જશે.", "ceo");
    }});
  }}
  else if(type === 'all') {{
    logMsg("Chief", "આજનો ઓલ-ઓવર 360° એક્ઝિક્યુટિવ રિપોર્ટ આપો.", "user");
    logMsg("👑 CEO", `<b>⭐ 360° EXECUTIVE AUDIT ({p_name}):</b><br>🔴 <b>Home Village:</b> TH{th_lvl} - ૧ બિલ્ડર ટૂંક સમયમાં ફ્રી થશે.<br>🟠 <b>War:</b> {clan_name} માં ૯૪% વિનિંગ પ્રોબેબિલિટી.<br>🟢 <b>Capital:</b> તમામ ૬ રેઇડ અટેક્સ પૂર્ણ થયેલા છે.`, "ceo");
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
    logMsg("👑 CEO", `Chief {p_name}, તમારો સંદેશ મળ્યો: "${{val}}". હું પટાવાળા દ્વારા આ ટાસ્ક સંબંધિત મેનેજર સુધી પહોંચાડી રહ્યો છું.`, "ceo");
  }}
}}

drawOffice();
</script>
</body>
</html>
"""

st.components.v1.html(app_html, height=860, scrolling=False)
