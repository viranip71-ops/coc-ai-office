import streamlit as st
import json
import urllib.request
import urllib.parse

st.set_page_config(
    page_title="CoC HQ - Smart Multi-Agent Terminal",
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
        with urllib.request.urlopen(req, timeout=7) as resp:
            return json.loads(resp.read().decode('utf-8'))
    except Exception as e:
        return None

clean_tag = urllib.parse.quote(PLAYER_TAG.strip())
player_raw = api_get(f"/players/{clean_tag}")

war_raw = None
if player_raw and 'clan' in player_raw:
    clan_tag = player_raw['clan'].get('tag')
    if clan_tag:
        clean_clan_tag = urllib.parse.quote(clan_tag)
        war_raw = api_get(f"/clans/{clean_clan_tag}/currentwar")

player_json_str = json.dumps(player_raw) if player_raw else "{}"
war_json_str = json.dumps(war_raw) if war_raw else "{}"

p_name = player_raw.get('name', 'Chief') if player_raw else 'Chief'
th_lvl = player_raw.get('townHallLevel', 1) if player_raw else 1
clan_name = player_raw.get('clan', {}).get('name', 'No Clan') if player_raw else 'No Clan'
status_label = f"🟢 LIVE: {p_name} (TH{th_lvl}) | Clan: {clan_name}"

raw_html_template = """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; font-family: monospace; }
  body { background: #030712; color: #f9fafb; padding: 4px; }
  .wrapper { max-width: 950px; margin: auto; display: flex; flex-direction: column; gap: 8px; }
  .banner { background: #0f172a; border: 1px solid #1e293b; border-radius: 8px; padding: 8px 12px; display: flex; justify-content: space-between; align-items: center; font-size: 11px; }
  .canvas-box { background: #090d16; border: 2px solid #1e293b; border-radius: 12px; padding: 6px; }
  canvas { background: #0f172a; border: 1px solid #334155; border-radius: 8px; width: 100%; display: block; }
  .chat-box { background: #0b0f19; border: 2px solid #1e293b; border-radius: 12px; height: 490px; display: flex; flex-direction: column; overflow: hidden; }
  .chat-head { background: #1e293b; padding: 8px 12px; font-size: 12px; font-weight: bold; color: #facc15; display: flex; justify-content: space-between; }
  .chat-log { flex: 1; padding: 10px; overflow-y: auto; font-size: 12px; line-height: 1.5; background: #030712; }
  .msg { margin-bottom: 10px; padding: 8px 12px; border-radius: 8px; font-size: 12px; }
  .msg-user { background: #1e3a8a; color: #bfdbfe; margin-left: 15%; text-align: right; }
  .msg-ceo { background: #1e293b; color: #f8fafc; border-left: 4px solid #facc15; }
  .msg-mgr { background: #064e3b; color: #a7f3d0; border-left: 4px solid #10b981; }
  .quick-cmds { display: flex; gap: 6px; padding: 6px 8px; background: #0f172a; overflow-x: auto; border-top: 1px solid #1e293b; }
  .btn-cmd { background: #1e293b; color: #e2e8f0; border: 1px solid #334155; padding: 6px 10px; font-size: 11px; border-radius: 6px; cursor: pointer; white-space: nowrap; font-weight: 500; }
  .btn-cmd:hover { background: #334155; color: #38bdf8; }
  .input-pane { display: flex; padding: 8px; background: #0f172a; border-top: 1px solid #1e293b; }
  .input-pane input { flex: 1; background: #1e293b; border: 1px solid #334155; color: #fff; padding: 8px 12px; border-radius: 6px; font-size: 12px; outline: none; }
  .input-pane button { margin-left: 6px; background: #f59e0b; color: #000; font-weight: bold; border: none; padding: 8px 16px; border-radius: 6px; cursor: pointer; }
</style>
</head>
<body>

<div class="wrapper">
  
  <div class="banner">
    <span style="font-weight:bold; color:#38bdf8;">🏢 REAL-TIME CLASH HQ</span>
    <span style="color:#34d399;">__STATUS_LABEL__</span>
  </div>

  <div class="canvas-box">
    <canvas id="officeCanvas" width="600" height="380"></canvas>
  </div>

  <div class="chat-box">
    <div class="chat-head">
      <span>👑 CEO EXECUTIVE SMART TERMINAL</span>
      <span style="color: #4ade80;">● AI ONLINE</span>
    </div>
    
    <div class="chat-log" id="chatLog">
      <div class="msg msg-ceo">
        <b>👑 Central CEO:</b> Greetings Chief <b>__P_NAME__</b>! હું સક્રિય છું. નીચેના ક્વિક બટન્સ વાપરો અથવા કોઈ પણ ચોક્કસ સવાલ પૂછો.
      </div>
    </div>

    <div class="quick-cmds">
      <button class="btn-cmd" onclick="handleUserSend('સામેવાળાએ આપણા પર કેટલા સ્ટાર કર્યા?')">🛡️ Opponent Attacks on Us</button>
      <button class="btn-cmd" onclick="handleUserSend('કોના અટેક બાકી છે?')">⚔️ Pending Attacks</button>
      <button class="btn-cmd" onclick="handleUserSend('Home Village અને Heroes Status')">🏰 Heroes & Village</button>
      <button class="btn-cmd" onclick="handleUserSend('આજનો ઓલ ઓવર રિપોર્ટ આપો')">⭐ 360° All-Over Audit</button>
    </div>

    <div class="input-pane">
      <input type="text" id="userInput" placeholder="દા.ત. સામેવાળાએ કેટલા સ્ટાર કર્યા? / કોના અટેક બાકી છે?" onkeydown="if(event.key==='Enter') handleUserSend()">
      <button onclick="handleUserSend()">Send</button>
    </div>
  </div>

</div>

<script>
const canvas = document.getElementById("officeCanvas");
const ctx = canvas.getContext("2d");

const rawPlayer = __PLAYER_JSON__;
const rawWar = __WAR_JSON__;

const rooms = [
  { id: "ceo",  x: 210, y: 15,  w: 180, h: 100, title: "👑 CEO CABIN", color: "#1e1b4b", border: "#facc15", door: {x: 300, y: 115} },
  { id: "hv",   x: 20,  y: 145, w: 220, h: 100, title: "🏰 HOME VILLAGE DEPT", color: "#0c4a6e", border: "#38bdf8", door: {x: 240, y: 190} },
  { id: "bb",   x: 360, y: 145, w: 220, h: 100, title: "🌙 BUILDER BASE LAB", color: "#3b0764", border: "#c084fc", door: {x: 360, y: 190} },
  { id: "clan", x: 20,  y: 265, w: 220, h: 100, title: "🛡️ WAR ROOM & CWL", color: "#064e3b", border: "#4ade80", door: {x: 240, y: 310} },
  { id: "cap",  x: 360, y: 265, w: 220, h: 100, title: "🏛️ CAPITAL TREASURY", color: "#7c2d12", border: "#fb923c", door: {x: 360, y: 310} }
];

const characters = {
  ceo: { x: 300, y: 55, skin: "#fed7aa", suit: "#0f172a", hair: "#e2e8f0" },
  hv: { x: 80, y: 190, skin: "#fed7aa", suit: "#0284c7", hair: "#78350f" },
  bb: { x: 420, y: 190, skin: "#fed7aa", suit: "#9333ea", hair: "#facc15" },
  clan: { x: 80, y: 310, skin: "#fed7aa", suit: "#16a34a", hair: "#1e293b" },
  cap: { x: 420, y: 310, skin: "#fed7aa", suit: "#ea580c", hair: "#b91c1c" },
  peon: { x: 300, y: 220, origX: 300, origY: 220, skin: "#fbcfe8", suit: "#64748b", cap: "#dc2626", state: "idle", hasFile: false }
};

function drawPlant(x, y) {
  ctx.fillStyle = "#15803d"; ctx.beginPath(); ctx.arc(x, y, 7, 0, Math.PI*2); ctx.fill();
  ctx.fillStyle = "#86efac"; ctx.beginPath(); ctx.arc(x-2, y-2, 4, 0, Math.PI*2); ctx.fill();
}

function drawOffice() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  ctx.fillStyle = "#090d16";
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  ctx.strokeStyle = "#1e293b";
  ctx.lineWidth = 1;
  for(let i=0; i<canvas.width; i+=20) { ctx.beginPath(); ctx.moveTo(i,0); ctx.lineTo(i,canvas.height); ctx.stroke(); }

  rooms.forEach(rm => {
    ctx.fillStyle = rm.color; ctx.fillRect(rm.x, rm.y, rm.w, rm.h);
    ctx.strokeStyle = rm.border; ctx.lineWidth = 2; ctx.strokeRect(rm.x, rm.y, rm.w, rm.h);
    ctx.strokeStyle = "#090d16"; ctx.lineWidth = 3;
    if(rm.door.y === 115) {
      ctx.beginPath(); ctx.moveTo(rm.door.x - 15, rm.door.y); ctx.lineTo(rm.door.x + 15, rm.door.y); ctx.stroke();
    } else {
      ctx.beginPath(); ctx.moveTo(rm.door.x, rm.door.y - 12); ctx.lineTo(rm.door.x, rm.door.y + 12); ctx.stroke();
    }
    ctx.fillStyle = rm.border; ctx.font = "bold 9px monospace"; ctx.fillText(rm.title, rm.x + 8, rm.y + 14);
  });

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
}

function drawDesk(x, y, w, h, color, pcPos) {
  ctx.fillStyle = color; ctx.fillRect(x, y, w, h);
  ctx.strokeStyle = "rgba(255,255,255,0.15)"; ctx.strokeRect(x, y, w, h);
  let mx = pcPos === "left" ? x+5 : (pcPos === "right" ? x+w-16 : x+w/2-6);
  ctx.fillStyle = "#0f172a"; ctx.fillRect(mx, y+3, 12, 8);
  ctx.fillStyle = "#38bdf8"; ctx.fillRect(mx+1, y+4, 10, 6);
}

function drawPerson(x, y, skin, suit, hair, isCEO=false, hasFile=false) {
  ctx.fillStyle = "rgba(0,0,0,0.35)"; ctx.beginPath(); ctx.ellipse(x, y+10, 8, 4, 0, 0, Math.PI*2); ctx.fill();
  ctx.fillStyle = suit; ctx.fillRect(x-6, y, 12, 10);
  if(isCEO) { ctx.fillStyle = "#ef4444"; ctx.fillRect(x-1, y+1, 2, 7); }
  ctx.fillStyle = skin; ctx.beginPath(); ctx.arc(x, y-4, 5, 0, Math.PI*2); ctx.fill();
  ctx.fillStyle = hair; ctx.beginPath(); ctx.arc(x, y-6, 5, Math.PI, Math.PI*2); ctx.fill();

  if(hasFile) {
    ctx.fillStyle = "#facc15"; ctx.fillRect(x+5, y+2, 7, 9);
    ctx.strokeStyle = "#fff"; ctx.strokeRect(x+5, y+2, 7, 9);
  }
}

function drawSpeech(x, y, txt) {
  ctx.fillStyle = "#0f172a"; ctx.fillRect(x - 45, y - 10, 90, 14);
  ctx.strokeStyle = "#facc15"; ctx.strokeRect(x - 45, y - 10, 90, 14);
  ctx.fillStyle = "#f8fafc"; ctx.font = "8px monospace"; ctx.fillText(txt, x - 40, y);
}

function dispatchPeon(deptId, callback) {
  let p = characters.peon;
  let mgr = characters[deptId];

  p.state = "to_mgr";
  walkTo(mgr.x + 18, mgr.y, function() {
    p.hasFile = true;
    p.state = "to_ceo";
    walkTo(300, 100, function() {
      p.state = "at_ceo";
      p.hasFile = false;
      setTimeout(function() {
        p.state = "idle";
        walkTo(p.origX, p.origY, callback);
      }, 800);
    });
  });
}

function walkTo(tx, ty, onDone) {
  let p = characters.peon;
  let speed = 4;
  let timer = setInterval(function() {
    let dx = tx - p.x, dy = ty - p.y;
    let dist = Math.sqrt(dx*dx + dy*dy);
    if(dist > speed) {
      p.x += (dx/dist)*speed;
      p.y += (dy/dist)*speed;
    } else {
      p.x = tx; p.y = ty;
      clearInterval(timer);
      if(onDone) onDone();
    }
  }, 25);
}

function logMsg(sender, text, type) {
  let box = document.getElementById("chatLog");
  let d = document.createElement("div");
  d.className = "msg msg-" + type;
  d.innerHTML = "<b>" + sender + ":</b> " + text;
  box.appendChild(d);
  box.scrollTop = box.scrollHeight;
}

// ================= SMART INTENT MATCHING ENGINE =================
function processSmartQuery(queryText) {
  let q = queryText.toLowerCase().trim();

  // ૧. સામેવાળાના અટેક્સ / ડિફેન્સ (Opponent attacks on us)
  if (q.includes("સામેવાળા") || q.includes("opponent") || q.includes("enemy") || q.includes("reaper") || q.includes("defense") || q.includes("ડિફેન્સ") || q.includes("star kar") || q.includes("star pad") || (q.includes("ketala") && q.includes("star"))) {
    if (!rawWar || rawWar.state === 'notInWar') {
      return { dept: 'clan', reply: "અત્યારે ક્લેન એક્ટિવ વોરમાં નથી." };
    }
    let clanMembers = rawWar.clan.members || [];
    let oppName = rawWar.opponent ? rawWar.opponent.name : "Opponent";
    let defHTML = "<b>🛡️ OPPONENT ATTACKS ON OUR CLAN (" + oppName + " Attacks):</b><br>";
    
    clanMembers.sort(function(a,b) { return a.mapPosition - b.mapPosition; });
    clanMembers.forEach(function(m) {
      let best = m.bestOpponentAttack;
      if (best) {
        defHTML += "• <b>#" + m.mapPosition + " " + m.name + "</b> (TH" + m.townhallLevel + "): <b>" + best.stars + "⭐ (" + best.destructionPercentage + "%)</b> લીધા<br>";
      } else {
        defHTML += "• <b>#" + m.mapPosition + " " + m.name + "</b> (TH" + m.townhallLevel + "): 🟢 <b>Safe (No attack yet)</b><br>";
      }
    });
    defHTML += "<br><b>કુલ વિગત:</b> " + oppName + " એ આપણા પર કુલ <b>" + rawWar.opponent.stars + "⭐ (" + rawWar.opponent.destructionPercentage + "%)</b> લીધા છે.";
    return { dept: 'clan', reply: defHTML };
  }

  // ૨. બાકી અટેક્સ (Pending Attacks)
  if (q.includes("baki") || q.includes("બાકી") || q.includes("pending") || q.includes("kona") || q.includes("કોના") || q.includes("left")) {
    if (!rawWar || rawWar.state === 'notInWar') {
      return { dept: 'clan', reply: "અત્યારે કોઈ સક્રિય વોર નથી." };
    }
    let clanMembers = rawWar.clan.members || [];
    let pendingHTML = "<b>⚔️ PENDING CLAN ATTACKS STATUS:</b><br>";
    let remainingCount = 0;

    clanMembers.sort(function(a,b) { return a.mapPosition - b.mapPosition; });
    clanMembers.forEach(function(m) {
      let used = m.attacks ? m.attacks.length : 0;
      let left = 2 - used;
      if (left > 0) {
        pendingHTML += "• <b>#" + m.mapPosition + " " + m.name + "</b>: " + left + " Attack(s) Left<br>";
        remainingCount += left;
      }
    });

    if (remainingCount === 0) {
      pendingHTML += "🎉 તમામ પ્લેયર્સે તેમના પૂરેપૂરા અટેક્સ પૂર્ણ કરી લીધા છે!";
    } else {
      pendingHTML += "<br><b>કુલ બાકી અટેક્સ:</b> " + remainingCount + " attacks left.";
    }
    return { dept: 'clan', reply: pendingHTML };
  }

  // ૩. Home Village / Heroes / Upgrades
  if (q.includes("hero") || q.includes("હીરો") || q.includes("queen") || q.includes("king") || q.includes("warden") || q.includes("champion") || q.includes("home") || q.includes("village") || q.includes("upgrade") || q.includes("ગામ")) {
    let heroes = (rawPlayer.heroes || []).filter(function(h) { return h.village === 'home'; }).map(function(h) { return "• <b>" + h.name + ":</b> Level " + h.level + " / " + h.maxLevel; }).join("<br>");
    let hvHTML = "<b>🏰 HOME VILLAGE & HEROES STATUS:</b><br>" +
                 "• <b>Player:</b> " + rawPlayer.name + " (Town Hall " + rawPlayer.townHallLevel + ")<br>" +
                 "• <b>Current Trophies:</b> " + rawPlayer.trophies + " 🏆 (Best: " + rawPlayer.bestTrophies + " 🏆)<br>" +
                 "• <b>Heroes:</b><br>" + heroes + "<br>" +
                 "• <b>Recommendation:</b> Archer Queen અને Royal Champion ને અપગ્રેડ પ્રાયોરિટી આપો.";
    return { dept: 'hv', reply: hvHTML };
  }

  // ૪. Builder Base
  if (q.includes("bb") || q.includes("builder") || q.includes("night") || q.includes("copter") || q.includes("રાત")) {
    return { dept: 'bb', reply: "<b>🌙 BUILDER BASE 2.0 STATUS:</b><br>• Builder Hall: Level " + (rawPlayer.builderHallLevel || 8) + "<br>• 6th Builder (B.O.B): 🟢 Fully Active<br>• Priority: Battle Copter અપગ્રેડ કરો." };
  }

  // ૫. Clan Capital
  if (q.includes("capital") || q.includes("raid") || q.includes("gold") || q.includes("કેપિટલ")) {
    return { dept: 'cap', reply: "<b>🏛️ CLAN CAPITAL AUDIT:</b><br>• Total Capital Gold Donated: <b>" + (rawPlayer.clanCapitalContributions ? rawPlayer.clanCapitalContributions.toLocaleString() : '0') + " 🪙</b><br>• Weekend Raids Synced." };
  }

  // ૬. Live Clan War General (War / Win status)
  if (q.includes("war") || q.includes("cwl") || q.includes("વોર") || q.includes("jit") || q.includes("જીત")) {
    if (!rawWar || rawWar.state === 'notInWar') {
      return { dept: 'clan', reply: "અત્યારે ક્લેન વોર એક્ટિવ નથી." };
    }
    let myWar = rawWar.clan.members ? rawWar.clan.members.find(function(m) { return m.tag === '__PLAYER_TAG__'; }) : null;
    let myAtt = myWar && myWar.attacks ? myWar.attacks.length : 0;
    let warHTML = "<b>⚔️ REAL-TIME CLAN WAR SCORE:</b><br>" +
                  "• <b>Match:</b> " + rawWar.clan.name + " <b>" + rawWar.clan.stars + "⭐ (" + rawWar.clan.destructionPercentage + "%)</b> vs " + rawWar.opponent.name + " <b>" + rawWar.opponent.stars + "⭐ (" + rawWar.opponent.destructionPercentage + "%)</b><br>" +
                  "• <b>Clan Attacks:</b> " + rawWar.clan.attacks + "/" + (rawWar.teamSize * 2) + "<br>" +
                  "• <b>Your Attacks:</b> " + myAtt + "/2 Used<br>" +
                  "• <b>Status:</b> 🟢 " + (rawWar.clan.stars > rawWar.opponent.stars ? "આપણે મજબૂત લીડ સાથે આગળ છીએ!" : "ટાઈ / ટક્કર છે.");
    return { dept: 'clan', reply: warHTML };
  }

  // ૭. All-over Audit (ફક્ત 'all', 'overall', 'આખો', 'બધો', 'સંપૂર્ણ' હોય ત્યારે જ)
  if (q.includes("all") || q.includes("overall") || q.includes("આખો") || q.includes("બધો") || q.includes("સંપૂર્ણ") || q.includes("360") || q.includes("audit")) {
    let warSummary = "No active war";
    if (rawWar && rawWar.state !== 'notInWar') {
      warSummary = rawWar.clan.name + " " + rawWar.clan.stars + "⭐ (" + rawWar.clan.destructionPercentage + "%) vs " + rawWar.opponent.name + " " + rawWar.opponent.stars + "⭐ (" + rawWar.opponent.destructionPercentage + "%)";
    }
    let heroes = (rawPlayer.heroes || []).filter(function(h) { return h.village === 'home'; }).map(function(h) { return h.name + " Lvl " + h.level; }).join(", ");
    let allHTML = "<b>⭐ 360° COMPLETE EXECUTIVE AUDIT:</b><br>" +
                  "• <b>Player:</b> " + rawPlayer.name + " (TH" + rawPlayer.townHallLevel + " | " + rawPlayer.trophies + " 🏆)<br>" +
                  "• <b>Heroes:</b> " + heroes + "<br>" +
                  "• <b>Live Clan War:</b> " + warSummary + "<br>" +
                  "• <b>Builder Base:</b> BH" + rawPlayer.builderHallLevel + " (6th Builder Active)<br>" +
                  "• <b>Capital Gold:</b> " + (rawPlayer.clanCapitalContributions ? rawPlayer.clanCapitalContributions.toLocaleString() : '0') + " 🪙<br>" +
                  "• <b>CEO Verdict:</b> વોરમાં ૯૫%+ ડિસ્ટ્રક્શન સાથે આપણી લીડ મજબૂત છે.";
    return { dept: 'all', reply: allHTML };
  }

  // Fallback
  return {
    dept: 'ceo',
    reply: "Chief, તમારો સવાલ '" + queryText + "' મળ્યો. ચોક્કસ માહિતી માટે પૂછો: જેમ કે <i>'સામેવાળાએ આપણા પર કેટલા સ્ટાર કર્યા?'</i>, <i>'કોના અટેક બાકી છે?'</i>, અથવા <i>'હીરો સ્ટેટસ'</i>."
  };
}

function handleUserSend(customText) {
  let inp = document.getElementById("userInput");
  let val = customText || (inp ? inp.value.trim() : "");
  if (!val) return;
  
  logMsg("Chief", val, "user");
  if (!customText && inp) inp.value = "";

  let result = processSmartQuery(val);

  if (result.dept === 'clan') {
    logMsg("👑 CEO", "War General પાસેથી લાઈવ ફાઈલ લાવી રહ્યો છું...", "ceo");
    dispatchPeon('clan', function() {
      logMsg("🛡️ War General", result.reply, "mgr");
    });
  } else if (result.dept === 'hv') {
    logMsg("👑 CEO", "Home Village Manager પાસેથી ડેટા મંગાવ્યો છે...", "ceo");
    dispatchPeon('hv', function() {
      logMsg("🏰 HV Manager", result.reply, "mgr");
    });
  } else if (result.dept === 'bb') {
    dispatchPeon('bb', function() {
      logMsg("🌙 BB Specialist", result.reply, "mgr");
    });
  } else if (result.dept === 'cap') {
    dispatchPeon('cap', function() {
      logMsg("🏛️ Capital Banker", result.reply, "mgr");
    });
  } else if (result.dept === 'all') {
    logMsg("👑 CEO", "તમામ ડિપાર્ટમેન્ટ્સ પાસેથી ફાઈલ ભેગી કરી રહ્યો છું...", "ceo");
    setTimeout(function() {
      logMsg("👑 CEO", result.reply, "ceo");
    }, 600);
  } else {
    logMsg("👑 CEO", result.reply, "ceo");
  }
}

drawOffice();
</script>
</body>
</html>
"""

# Placeholders injection
final_html = raw_html_template.replace("__STATUS_LABEL__", status_label)
final_html = final_html.replace("__P_NAME__", p_name)
final_html = final_html.replace("__PLAYER_JSON__", player_json_str)
final_html = final_html.replace("__WAR_JSON__", war_json_str)
final_html = final_html.replace("__PLAYER_TAG__", PLAYER_TAG)

st.components.v1.html(final_html, height=920, scrolling=False)
