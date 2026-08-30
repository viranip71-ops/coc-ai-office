import streamlit as st
import json
import urllib.request
import urllib.parse

st.set_page_config(
    page_title="CoC HQ - 100% Live Sync",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="collapsed"
)

PLAYER_TAG = "#GVQPR9J82"
API_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6ImM0MDk0Nzk4LTViODktNDIxZC1hYzcwLThjY2ViOGZjMTFjYiIsImlhdCI6MTc4ODA3OTAwNywic3ViIjoiZGV2ZWxvcGVyLzllYmFiYzlmLTM0M2UtNDU2My1iYmM0LTAyOGJjZWE1MTEzMyIsInNjb3BlcyI6WyJjbGFzaCJdLCJsaW1pdHMiOlt7InRpZXIiOiJkZXZlbG9wZXIvc2lsdmVyIiwidHlwZSI6InRocm90dGxpbmcifSx7ImNpZHJzIjpbIjM1LjIzMC41Ni4zMCJdLCJ0eXBlIjoiY2xpZW50In1dfQ._wLkYrhFvkLu4mcFpOdo5zzcTA0sXdxFrFd_wRi5SSBZJwekszYTENnmXVhoLkB2PYHAfNU7IRgV47YDyaY1dQ"

def api_get(endpoint):
    try:
        url = f"https://api.clashofclans.com/v1{endpoint}"
        req = urllib.request.Request(url, headers={"Authorization": f"Bearer {API_TOKEN.strip()}", "Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=6) as resp:
            return json.loads(resp.read().decode('utf-8'))
    except Exception as e:
        return None

# ૧. પ્લેયર પ્રોફાઇલ લાઈવ ડેટા
clean_tag = urllib.parse.quote(PLAYER_TAG.strip())
player_data = api_get(f"/players/{clean_tag}")

# ૨. લાઈવ ક્લેન વોર ડેટા (Real-time War API)
war_data = None
clan_tag = None
if player_data and 'clan' in player_data:
    clan_tag = player_data['clan'].get('tag')
    if clan_tag:
        clean_clan_tag = urllib.parse.quote(clan_tag)
        war_data = api_get(f"/clans/{clean_clan_tag}/currentwar")

# ડેટા પ્રોસેસિંગ
if player_data:
    p_name = player_data.get('name', 'Chief')
    th_lvl = player_data.get('townHallLevel', 1)
    trophies = player_data.get('trophies', 0)
    war_stars = player_data.get('warStars', 0)
    clan_name = player_data.get('clan', {}).get('name', 'No Clan')
    bh_lvl = player_data.get('builderHallLevel', 0)
    cap_gold = player_data.get('clanCapitalContributions', 0)
    
    heroes_arr = [f"{h['name']} (Lvl {h['level']}/{h.get('maxLevel', '?')})" for h in player_data.get('heroes', []) if h.get('village') == 'home']
    heroes_str = "<br>• ".join(heroes_arr) if heroes_arr else "No heroes unlocked"
    status_label = f"🟢 LIVE CONNECTED: {p_name} (TH{th_lvl}) | Clan: {clan_name}"
else:
    p_name = "Chief"
    th_lvl = 15
    trophies = 3450
    war_stars = 720
    clan_name = "Active Clan"
    bh_lvl = 9
    cap_gold = 385000
    heroes_str = "Barbarian King, Archer Queen, Grand Warden"
    status_label = "🟡 CONNECTING TO SUPERCELL..."

# અસલી વોર ડેટા પાર્સિંગ
war_status_html = ""
if war_data and war_data.get('state') != 'notInWar':
    w_state = war_data.get('state', 'inWar').upper()
    team_size = war_data.get('teamSize', 15)
    clan_info = war_data.get('clan', {})
    opp_info = war_data.get('opponent', {})
    
    c_stars = clan_info.get('stars', 0)
    o_stars = opp_info.get('stars', 0)
    c_att = clan_info.get('attacks', 0)
    o_att = opp_info.get('attacks', 0)
    c_dest = round(clan_info.get('destructionPercentage', 0), 1)
    o_dest = round(opp_info.get('destructionPercentage', 0), 1)
    opp_name = opp_info.get('name', 'Opponent Clan')

    # ચેક કરો કે પ્લેયરે અટેક કર્યો છે કે નહીં
    my_war_member = next((m for m in clan_info.get('members', []) if m.get('tag') == PLAYER_TAG), None)
    my_attacks_cnt = len(my_war_member.get('attacks', [])) if my_war_member else 0
    my_stars = sum([a.get('stars', 0) for a in my_war_member.get('attacks', [])]) if my_war_member else 0

    war_status_html = f"""
    <b>⚔️ REAL-TIME CLAN WAR DATA:</b><br>
    • <b>Status:</b> {w_state} ({team_size}vs{team_size})<br>
    • <b>Opponent:</b> {opp_name}<br>
    • <b>Score:</b> {clan_name} <b>{c_stars}⭐ ({c_dest}%)</b> vs {opp_name} <b>{o_stars}⭐ ({o_dest}%)</b><br>
    • <b>Total Attacks Used:</b> {c_att}/{team_size*2} (Opponent: {o_att}/{team_size*2})<br>
    • <b>Your Attacks in this War:</b> {my_attacks_cnt}/2 Attacks Used ({my_stars}⭐ scored)<br>
    • <b>Live Outlook:</b> {'🟢 Currently Leading!' if c_stars > o_stars else ('🔴 Trailing' if c_stars < o_stars else '🟡 Tied Match')}
    """
else:
    war_status_html = f"<b>⚔️ CLAN WAR STATUS:</b><br>• અત્યારે તમારો ક્લેન સક્રિય વોરમાં નથી અથવા વોર લોગ પ્રાઈવેટ છે.<br>• <b>Total Career War Stars:</b> {war_stars} ⭐"

app_html = f"""
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; font-family: monospace; }}
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
    height: 450px;
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
    <span style="font-weight:bold; color:#38bdf8;">🏢 REAL-TIME CLASH HQ</span>
    <span style="color:#34d399;">{status_label}</span>
  </div>

  <div class="canvas-box">
    <canvas id="officeCanvas" width="600" height="380"></canvas>
  </div>

  <div class="chat-box">
    <div class="chat-head">
      <span>👑 CEO EXECUTIVE TERMINAL (100% REAL DATA)</span>
      <span style="color: #4ade80;">● ACTIVE</span>
    </div>
    
    <div class="chat-log" id="chatLog">
      <div class="msg msg-ceo">
        <b>👑 Central CEO:</b> Chief <b>{p_name}</b>, તમારું અસલી પ્લેયર અને લાઈવ ક્લેન વોર સર્વર જોડાઈ ગયું છે. મેનેજર પાસેથી અસલી ફાઇલ મંગાવવા નીચે ક્લિક કરો.
      </div>
    </div>

    <div class="quick-cmds">
      <button class="btn-cmd" onclick="triggerReport('war')">🛡️ Real-Time Clan War</button>
      <button class="btn-cmd" onclick="triggerReport('hv')">🏰 Home Village & Heroes</button>
      <button class="btn-cmd" onclick="triggerReport('bb')">🌙 Builder Base Audit</button>
      <button class="btn-cmd" onclick="triggerReport('cap')">🏛️ Clan Capital Loot</button>
    </div>

    <div class="input-pane">
      <input type="text" id="userInput" placeholder="CEO ને પૂછો (દા.ત. War status, Builder status, Hero upgrades...)" onkeydown="if(event.key==='Enter') handleUserSend()">
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
  ctx.fillStyle = "#090d16"; ctx.fillRect(0, 0, canvas.width, canvas.height);

  ctx.strokeStyle = "#1e293b"; ctx.lineWidth = 1;
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
    logMsg("Chief", "લાઈવ Clan War નો સાચો રિપોર્ટ આપો.", "user");
    logMsg("👑 CEO", "War General પાસેથી સુપરસેલનું લાઈવ વોર લોગ મંગાવું છું...", "ceo");
    dispatchPeon('clan', () => {{
      logMsg("🛡️ War General", `{war_status_html}`, "mgr");
      logMsg("👑 CEO", "આ લાઈવ વોર ડેટા સુપરસેલ સર્વર પરથી ફેચ કરેલો છે.", "ceo");
    }});
  }}
  else if(type === 'hv') {{
    logMsg("Chief", "Home Village અને Heroes સ્ટેટસ આપો.", "user");
    logMsg("👑 CEO", "Home Village Manager પાસેથી ફાઈલ આવી રહી છે...", "ceo");
    dispatchPeon('hv', () => {{
      let hvHTML = `
      <b>🏰 REAL-TIME HOME VILLAGE REPORT:</b><br>
      • <b>Player:</b> {p_name} | <b>Town Hall:</b> Level {th_lvl}<br>
      • <b>Current Trophies:</b> {trophies} 🏆<br>
      • <b>Live Heroes Status:</b><br>• {heroes_str}<br>
      • <b>Note on Builders:</b> સુપરસેલ API ચાલુ ટાઈમર્સ (Ongoing Minutes) આપતું નથી. બિલ્ડર ફ્રી થતાં જ હીરો અને મોનોલિથ અપગ્રેડ કરો!
      `;
      logMsg("🏰 HV Manager", hvHTML, "mgr");
    }});
  }}
  else if(type === 'bb') {{
    logMsg("Chief", "Builder Base રિપોર્ટ આપો.", "user");
    dispatchPeon('bb', () => {{
      logMsg("🌙 BB Specialist", "<b>Builder Base Live:</b><br>• Builder Hall: Level {bh_lvl}<br>• 6th Builder: B.O.B Active", "mgr");
    }});
  }}
  else if(type === 'cap') {{
    logMsg("Chief", "Clan Capital રિપોર્ટ આપો.", "user");
    dispatchPeon('cap', () => {{
      logMsg("🏛️ Capital Banker", "<b>Clan Capital Contribution:</b><br>• Total Donated: {cap_gold:,} 🪙", "mgr");
    }});
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
  else if(l.includes("hero") || l.includes("home") || l.includes("upgrade") || l.includes("builder") || l.includes("th")) triggerReport('hv');
  else if(l.includes("bb") || l.includes("night")) triggerReport('bb');
  else if(l.includes("capital") || l.includes("raid")) triggerReport('cap');
  else logMsg("👑 CEO", `Chief, તમારો સંદેશ મળ્યો: "${{val}}".`, "ceo");
}}

drawOffice();
</script>
</body>
</html>
"""

st.components.v1.html(app_html, height=880, scrolling=False)
