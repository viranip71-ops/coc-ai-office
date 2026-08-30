import streamlit as st
import json
import urllib.request
import urllib.parse

st.set_page_config(
    page_title="CoC AI Office HQ",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="collapsed"
)

PLAYER_TAG = "#GVQPR9J82"
API_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjkzZDNkZTk3LTJmZmYtNDM5YS05NTgzLTM3NzZkMGZhMzc3NSIsImlhdCI6MTc4ODA3NDY5Niwic3ViIjoiZGV2ZWxvcGVyLzllYmFiYzlmLTM0M2UtNDU2My1iYmM0LTAyOGJjZWE1MTEzMyIsInNjb3BlcyI6WyJjbGFzaCJdLCJsaW1pdHMiOlt7InRpZXIiOiJkZXZlbG9wZXIvc2lsdmVyIiwidHlwZSI6InRocm90dGxpbmcifSx7ImNpZHJzIjpbIjM0LjkuMTQ0LjIyMCJdLCJ0eXBlIjoiY2xpZW50In1dfQ.C-AuXUoXnCJA6pazFYpYg0IUgivSctttnT7iJEZPyiAQj8tAlJ940xrbxTWQlU53EcROBzbOu8vpqDVpO_fvvA"

@st.cache_data(ttl=60)
def get_live_data():
    try:
        clean_tag = urllib.parse.quote(PLAYER_TAG)
        url = f"https://api.clashofclans.com/v1/players/{clean_tag}"
        req = urllib.request.Request(url, headers={"Authorization": f"Bearer {API_TOKEN.strip()}", "Accept": "application/json"})
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode('utf-8'))
    except Exception as e:
        return None

live_data = get_live_data()
p_name = live_data.get('name', 'Chief') if live_data else 'Chief'
th_lvl = live_data.get('townHallLevel', 15) if live_data else 15
trophies = live_data.get('trophies', 0) if live_data else 0
clan_title = live_data.get('clan', {}).get('name', 'Active Clan') if live_data else 'Active Clan'

ui_html = f"""
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; font-family: monospace; }}
  body {{ background: #0b0f19; color: #f8fafc; padding: 4px; }}
  
  .office-container {{
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
    max-width: 1100px;
    margin: auto;
    background: #111827;
    border: 2px solid #374151;
    border-radius: 12px;
    overflow: hidden;
  }}

  .canvas-pane {{
    flex: 1.2;
    min-width: 380px;
    background: #1f2937;
    border-right: 2px solid #374151;
    padding: 10px;
    display: flex;
    flex-direction: column;
    align-items: center;
  }}

  .pane-header {{
    width: 100%;
    display: flex;
    justify-content: space-between;
    padding: 6px 12px;
    background: #0f172a;
    border-radius: 6px;
    margin-bottom: 8px;
    font-size: 13px;
    color: #38bdf8;
    border: 1px solid #1e293b;
  }}

  canvas {{
    background: #182234;
    border: 2px solid #4b5563;
    border-radius: 8px;
    width: 100%;
    max-width: 440px;
    height: auto;
  }}

  .chat-pane {{
    flex: 1;
    min-width: 320px;
    background: #0f172a;
    display: flex;
    flex-direction: column;
    height: 480px;
  }}

  .terminal-header {{
    background: #1e293b;
    padding: 10px 14px;
    border-bottom: 2px solid #334155;
    display: flex;
    align-items: center;
    justify-content: space-between;
  }}

  .chat-log {{
    flex: 1;
    padding: 12px;
    overflow-y: auto;
    font-size: 12px;
    line-height: 1.5;
    background: #090d16;
  }}

  .msg {{ margin-bottom: 8px; padding: 6px 10px; border-radius: 6px; }}
  .msg-user {{ background: #1e3a8a; color: #bfdbfe; margin-left: auto; text-align: right; }}
  .msg-ceo {{ background: #1f2937; color: #f8fafc; border-left: 4px solid #facc15; }}
  .msg-manager {{ background: #132e27; color: #6ee7b7; border-left: 4px solid #10b981; }}

  .quick-bar {{
    display: flex;
    gap: 5px;
    padding: 6px;
    background: #1e293b;
    overflow-x: auto;
    border-top: 1px solid #334155;
  }}
  .btn-quick {{
    background: #334155;
    color: #fff;
    border: 1px solid #475569;
    padding: 5px 8px;
    font-size: 11px;
    border-radius: 4px;
    cursor: pointer;
    white-space: nowrap;
  }}

  .input-box {{
    display: flex;
    padding: 8px;
    background: #111827;
    border-top: 2px solid #1f2937;
  }}
  .input-box input {{
    flex: 1;
    background: #1f2937;
    border: 1px solid #374151;
    padding: 6px 10px;
    color: #fff;
    border-radius: 4px;
    font-size: 12px;
    outline: none;
  }}
  .input-box button {{
    margin-left: 6px;
    background: #f59e0b;
    color: #000;
    font-weight: bold;
    border: none;
    padding: 6px 12px;
    border-radius: 4px;
    cursor: pointer;
  }}
</style>
</head>
<body>

<div class="office-container">
  
  <div class="canvas-pane">
    <div class="pane-header">
      <span>🏢 <b>HQ VIRTUAL OFFICE</b></span>
      <span style="color: #4ade80;">{PLAYER_TAG}</span>
    </div>
    <canvas id="officeCanvas" width="440" height="390"></canvas>
  </div>

  <div class="chat-pane">
    <div class="terminal-header">
      <span style="color: #facc15; font-size: 13px; font-weight: bold;">👑 CEO EXECUTIVE CONSOLE</span>
      <span style="width: 10px; height: 10px; background: #22c55e; border-radius: 50%; display: inline-block;"></span>
    </div>
    
    <div class="chat-log" id="chatLog">
      <div class="msg msg-ceo">
        <b>👑 CEO:</b> Greetings Chief <b>{p_name}</b>! Town Hall {th_lvl} લાઈવ છે. નીચેથી કોઈપણ ડિપાર્ટમેન્ટનો રિપોર્ટ માંગો.
      </div>
    </div>

    <div class="quick-bar">
      <button class="btn-quick" onclick="requestReport('hv')">🏰 Home Village</button>
      <button class="btn-quick" onclick="requestReport('bb')">🌙 Builder Base</button>
      <button class="btn-quick" onclick="requestReport('clan')">🛡️ Clan</button>
      <button class="btn-quick" onclick="requestReport('cap')">🏛️ Capital</button>
    </div>

    <div class="input-box">
      <input type="text" id="userInput" placeholder="CEO ને સવાલ પૂછો અથવા ટાસ્ક આપો..." onkeydown="if(event.key==='Enter') sendMsg()">
      <button onclick="sendMsg()">Send</button>
    </div>
  </div>

</div>

<script>
const canvas = document.getElementById("officeCanvas");
const ctx = canvas.getContext("2d");

const agents = {{
  hv: {{ name: "Home Village", origX: 80, origY: 200, x: 80, y: 200, color: "#38bdf8", targetX: 180, targetY: 110, state: "idle" }},
  bb: {{ name: "Builder Base", origX: 350, origY: 200, x: 350, y: 200, color: "#c084fc", targetX: 250, targetY: 110, state: "idle" }},
  clan: {{ name: "Clan Manager", origX: 80, origY: 320, x: 80, y: 320, color: "#4ade80", targetX: 180, targetY: 120, state: "idle" }},
  cap: {{ name: "Clan Capital", origX: 350, origY: 320, x: 350, y: 320, color: "#fb923c", targetX: 250, targetY: 120, state: "idle" }}
}};

function drawOffice() {{
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  ctx.fillStyle = "#1e293b"; ctx.fillRect(0, 0, canvas.width, canvas.height);

  ctx.strokeStyle = "#334155"; ctx.lineWidth = 1;
  for(let x=0; x<canvas.width; x+=30) {{ ctx.beginPath(); ctx.moveTo(x,0); ctx.lineTo(x,canvas.height); ctx.stroke(); }}
  for(let y=0; y<canvas.height; y+=30) {{ ctx.beginPath(); ctx.moveTo(0,y); ctx.lineTo(canvas.width,y); ctx.stroke(); }}

  ctx.fillStyle = "#312e81"; ctx.fillRect(130, 15, 170, 90);
  ctx.strokeStyle = "#fbbf24"; ctx.lineWidth = 2; ctx.strokeRect(130, 15, 170, 90);
  ctx.fillStyle = "#78350f"; ctx.fillRect(175, 45, 80, 35);
  ctx.fillStyle = "#fbbf24"; ctx.font = "bold 10px monospace"; ctx.fillText("👑 CEO DESK", 182, 65);

  ctx.beginPath(); ctx.arc(215, 35, 11, 0, Math.PI*2); ctx.fillStyle = "#facc15"; ctx.fill();

  for(let k in agents) {{
    let ag = agents[k];
    ctx.fillStyle = "#475569"; ctx.fillRect(ag.origX - 30, ag.origY - 18, 60, 36);
    ctx.strokeStyle = ag.color; ctx.lineWidth = 2; ctx.strokeRect(ag.origX - 30, ag.origY - 18, 60, 36);
    ctx.fillStyle = "#f8fafc"; ctx.font = "9px monospace"; ctx.fillText(ag.name, ag.origX - 28, ag.origY + 28);

    ctx.beginPath(); ctx.arc(ag.x, ag.y, 10, 0, Math.PI*2); ctx.fillStyle = ag.color; ctx.fill();
    ctx.strokeStyle = "#fff"; ctx.stroke();
  }}
  requestAnimationFrame(drawOffice);
}}

function moveAgent(key, callback) {{
  let ag = agents[key];
  let speed = 4;
  let timer = setInterval(() => {{
    let dx = ag.targetX - ag.x, dy = ag.targetY - ag.y;
    let dist = Math.sqrt(dx*dx + dy*dy);
    if(dist > speed) {{
      ag.x += (dx/dist)*speed; ag.y += (dy/dist)*speed;
    }} else {{
      ag.x = ag.targetX; ag.y = ag.targetY;
      clearInterval(timer);
      setTimeout(() => {{
        let backTimer = setInterval(() => {{
          let bdx = ag.origX - ag.x, bdy = ag.origY - ag.y;
          let bdist = Math.sqrt(bdx*bdx + bdy*bdy);
          if(bdist > speed) {{
            ag.x += (bdx/bdist)*speed; ag.y += (bdy/bdist)*speed;
          }} else {{
            ag.x = ag.origX; ag.y = ag.origY;
            clearInterval(backTimer);
            if(callback) callback();
          }}
        }}, 25);
      }}, 1200);
    }}
  }}, 25);
}}

function addLog(sender, text, type) {{
  let box = document.getElementById("chatLog");
  let d = document.createElement("div");
  d.className = `msg msg-${{type}}`;
  d.innerHTML = `<b>${{sender}}:</b> ${{text}}`;
  box.appendChild(d);
  box.scrollTop = box.scrollHeight;
}}

function requestReport(dept) {{
  if(dept === 'hv') {{
    addLog("Chief", "Home Village નો રિપોર્ટ આપો.", "user");
    addLog("👑 CEO", "Home Village Manager રિપોર્ટ લઈને આવી રહ્યો છે...", "ceo");
    moveAgent('hv', () => {{
      addLog("🏰 HV Manager", `<b>Town Hall {th_lvl} Report:</b><br>• Trophies: {trophies} 🏆<br>• Priority: Hero Upgrades & Core Defences`, "manager");
      addLog("👑 CEO", "રિપોર્ટ મંજૂર છે. બિલ્ડર ફ્રી થતાં જ મોનોલિથ અને ક્વીન અપગ્રેડ કરો.", "ceo");
    }});
  }} else if(dept === 'bb') {{
    addLog("Chief", "Builder Base રિપોર્ટ આપો.", "user");
    addLog("👑 CEO", "Builder Base Manager કેબિનમાં બોલાવાયો છે...", "ceo");
    moveAgent('bb', () => {{
      addLog("🌙 BB Manager", "<b>Builder Base Brief:</b><br>• 6th Builder (B.O.B): Active<br>• Focus: Hero & Copter Level Up", "manager");
      addLog("👑 CEO", "બેટલ કોપ્ટર અપગ્રેડ ચાલુ રાખો.", "ceo");
    }});
  }} else if(dept === 'clan') {{
    addLog("Chief", "Clan રિપોર્ટ આપો.", "user");
    addLog("👑 CEO", "Clan Manager ફાઇલ સબમિટ કરવા આવી રહ્યો છે...", "ceo");
    moveAgent('clan', () => {{
      addLog("🛡️ Clan Manager", "<b>Clan: {clan_title}</b><br>• War Tracking & CWL Active", "manager");
      addLog("👑 CEO", "CWL બોનસ સારા પરફોર્મર્સને ફાળવવામાં આવશે.", "ceo");
    }});
  }} else if(dept === 'cap') {{
    addLog("Chief", "Capital Raid રિપોર્ટ આપો.", "user");
    addLog("👑 CEO", "Clan Capital Manager રિપોર્ટ સાથે હાજર થઈ રહ્યો છે...", "ceo");
    moveAgent('cap', () => {{
      addLog("🏛️ Capital Manager", "<b>Clan Capital:</b><br>• 6/6 Raids Used. Capital Gold Donated", "manager");
      addLog("👑 CEO", "ઉત્તમ યોગદાન!", "ceo");
    }});
  }}
}}

function sendMsg() {{
  let inp = document.getElementById("userInput");
  let val = inp.value.trim();
  if(!val) return;
  addLog("Chief", val, "user");
  inp.value = "";
  let l = val.toLowerCase();
  if(l.includes("home") || l.includes("hero") || l.includes("th")) requestReport('hv');
  else if(l.includes("builder") || l.includes("bb")) requestReport('bb');
  else if(l.includes("clan") || l.includes("war")) requestReport('clan');
  else if(l.includes("capital") || l.includes("raid")) requestReport('cap');
  else addLog("👑 CEO", `ટાસ્ક નોંધાઈ ગયો છે: "${{val}}". હું યોગ્ય મેનેજરને સૂચના આપી દઉં છું.`, "ceo");
}}

drawOffice();
</script>
</body>
</html>
"""

st.components.v1.html(ui_html, height=520, scrolling=False)
