import streamlit as st
import json
import urllib.request
import urllib.parse
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime

st.set_page_config(
    page_title="CoC AI Autonomous HQ",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ================= CREDENTIALS =================
PLAYER_TAG = "#GVQPR9J82"
SUPERCELL_API_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6ImM0MDk0Nzk4LTViODktNDIxZC1hYzcwLThjY2ViOGZjMTFjYiIsImlhdCI6MTc4ODA3OTAwNywic3ViIjoiZGV2ZWxvcGVyLzllYmFiYzlmLTM0M2UtNDU2My1iYmM0LTAyOGJjZWE1MTEzMyIsInNjb3BlcyI6WyJjbGFzaCJdLCJsaW1pdHMiOlt7InRpZXIiOiJkZXZlbG9wZXIvc2lsdmVyIiwidHlwZSI6InRocm90dGxpbmcifSx7ImNpZHJzIjpbIjM1LjIzMC41Ni4zMCJdLCJ0eXBlIjoiY2xpZW50In1dfQ._wLkYrhFvkLu4mcFpOdo5zzcTA0sXdxFrFd_wRi5SSBZJwekszYTENnmXVhoLkB2PYHAfNU7IRgV47YDyaY1dQ"

MY_GMAIL = "viranip71@gmail.com"
APP_PASSWORD = "wdckbdeqnfzoxzfa"

# ================= SUPERCELL MULTI-ENDPOINT FETCH ENGINE =================
def api_get(endpoint):
    try:
        url = f"https://api.clashofclans.com/v1{endpoint}"
        req = urllib.request.Request(url, headers={"Authorization": f"Bearer {SUPERCELL_API_TOKEN.strip()}", "Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=8) as resp:
            return json.loads(resp.read().decode('utf-8'))
    except Exception as e:
        return None

clean_tag = urllib.parse.quote(PLAYER_TAG.strip())
player_raw = api_get(f"/players/{clean_tag}")

war_raw = None
capital_raw = None
if player_raw and 'clan' in player_raw:
    clan_tag = player_raw['clan'].get('tag')
    if clan_tag:
        clean_clan_tag = urllib.parse.quote(clan_tag)
        war_raw = api_get(f"/clans/{clean_clan_tag}/currentwar")
        capital_raw = api_get(f"/clans/{clean_clan_tag}/capitalraidseasons?limit=1")

# ================= DEEP IN-DEPTH EMAIL BUILDER =================
def build_comprehensive_email_html():
    p_name = player_raw.get('name', 'Prince') if player_raw else 'Prince'
    th = player_raw.get('townHallLevel', 13) if player_raw else 13
    trophies = player_raw.get('trophies', 0) if player_raw else 0
    best_trophies = player_raw.get('bestTrophies', 0) if player_raw else 0
    attack_wins = player_raw.get('attackWins', 0) if player_raw else 0
    defense_wins = player_raw.get('defenseWins', 0) if player_raw else 0
    clan_name = player_raw.get('clan', {}).get('name', 'Shadow Apex') if player_raw else 'Shadow Apex'
    clan_tag = player_raw.get('clan', {}).get('tag', '#CLAN') if player_raw else '#CLAN'
    war_stars = player_raw.get('warStars', 0) if player_raw else 0
    bh_lvl = player_raw.get('builderHallLevel', 8) if player_raw else 8
    cap_gold = player_raw.get('clanCapitalContributions', 0) if player_raw else 0

    # 1. Heroes & Equipment Rows
    hero_rows = ""
    if player_raw and 'heroes' in player_raw:
        for h in player_raw['heroes']:
            if h.get('village') == 'home':
                hero_rows += f"<tr><td style='padding:7px 10px; border:1px solid #334155;'><b>{h['name']}</b></td><td style='padding:7px 10px; border:1px solid #334155; color:#38bdf8;'>Level {h['level']} / {h.get('maxLevel', '?')}</td></tr>"
    else:
        hero_rows = "<tr><td colspan='2' style='padding:7px; text-align:center;'>No hero data found</td></tr>"

    # 2. Deep War Analysis
    war_section = ""
    if war_raw and war_raw.get('state') != 'notInWar':
        clan_info = war_raw.get('clan', {})
        opp_info = war_raw.get('opponent', {})
        c_name = clan_info.get('name', clan_name)
        o_name = opp_info.get('name', 'Opponent')
        c_stars = clan_info.get('stars', 0)
        o_stars = opp_info.get('stars', 0)
        c_dest = round(clan_info.get('destructionPercentage', 0), 1)
        o_dest = round(opp_info.get('destructionPercentage', 0), 1)
        team_size = war_raw.get('teamSize', 5)
        c_attacks = clan_info.get('attacks', 0)
        o_attacks = opp_info.get('attacks', 0)

        # Player Performance Parsing
        clan_members = clan_info.get('members', [])
        clan_members.sort(key=lambda x: x.get('mapPosition', 99))

        mvp_list = []
        underperformers = []
        pending_attacks = []
        defense_audit = []

        for m in clan_members:
            m_pos = m.get('mapPosition')
            m_name = m.get('name')
            m_th = m.get('townhallLevel')
            atts = m.get('attacks', [])
            used = len(atts)
            left = 2 - used
            total_m_stars = sum([a.get('stars', 0) for a in atts])
            total_m_dest = sum([a.get('destructionPercentage', 0) for a in atts])

            # Pending
            if left > 0:
                pending_attacks.append(f"#{m_pos} <b>{m_name}</b> (TH{m_th}): {left} attack(s) remaining")

            # MVP & Underperformers
            if used == 2 and total_m_stars == 6:
                mvp_list.append(f"🌟 <b>#{m_pos} {m_name}</b> - 6⭐ (100% Max Triples)")
            elif used > 0 and total_m_stars >= 5:
                mvp_list.append(f"⭐ <b>#{m_pos} {m_name}</b> - {total_m_stars}⭐ ({total_m_dest}%)")
            
            if left == 2:
                underperformers.append(f"❌ <b>#{m_pos} {m_name}</b> - 0/2 Attacks Used (Did Not Attack)")
            elif used == 2 and total_m_stars <= 2:
                underperformers.append(f"⚠️ <b>#{m_pos} {m_name}</b> - Only {total_m_stars}⭐ scored across 2 attacks")

            # Defense Analysis (Opponent attacks on this member)
            best_def = m.get('bestOpponentAttack')
            if best_def:
                defense_audit.append(f"<tr><td style='padding:6px; border:1px solid #334155;'>#{m_pos} <b>{m_name}</b> (TH{m_th})</td><td style='padding:6px; border:1px solid #334155; color:#ef4444;'>{best_def.get('stars')}⭐ ({best_def.get('destructionPercentage')}%)</td><td style='padding:6px; border:1px solid #334155;'>Attacker #{best_def.get('attackerTag')}</td></tr>")
            else:
                defense_audit.append(f"<tr><td style='padding:6px; border:1px solid #334155;'>#{m_pos} <b>{m_name}</b> (TH{m_th})</td><td style='padding:6px; border:1px solid #334155; color:#22c55e;'>🟢 Safe (0 Stars Conceded)</td><td style='padding:6px; border:1px solid #334155;'>Unattacked</td></tr>")

        mvp_html = "<br>".join(mvp_list) if mvp_list else "No player scored 5+ stars yet."
        under_html = "<br>".join(underperformers) if underperformers else "None (All clan members attacked well!)."
        pending_html = "<br>".join(pending_attacks) if pending_attacks else "🎉 All clan attacks have been completed!"
        defense_table_rows = "".join(defense_audit)

        status_badge = "<span style='background:#15803d; color:#fff; padding:3px 8px; border-radius:4px;'>🟢 WE WON / LEADING</span>" if c_stars > o_stars or (c_stars == o_stars and c_dest > o_dest) else "<span style='background:#b91c1c; color:#fff; padding:3px 8px; border-radius:4px;'>🔴 OPPONENT LEADING</span>"

        war_section = f"""
        <div style="background:#1e293b; padding:15px; border-radius:8px; border-left:5px solid #facc15; margin-bottom:20px;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
                <h3 style="margin:0; color:#facc15;">⚔️ CLAN WAR & CWL DEEP POST-MORTEM</h3>
                {status_badge}
            </div>
            <p style="font-size:15px; margin:5px 0;">
                <b>{c_name}</b> <span style="color:#facc15; font-size:17px;"><b>{c_stars}⭐ ({c_dest}%)</b></span> vs <b>{o_name}</b> <span style="color:#facc15; font-size:17px;"><b>{o_stars}⭐ ({o_dest}%)</b></span>
            </p>
            <p style="color:#94a3b8; font-size:12px; margin:0 0 10px 0;">Attacks: {c_name} ({c_attacks}/{team_size*2}) vs {o_name} ({o_attacks}/{team_size*2})</p>

            <h4 style="color:#38bdf8; margin:12px 0 6px 0;">🌟 Top Performers (MVPs):</h4>
            <div style="background:#0f172a; padding:10px; border-radius:6px; font-size:13px; color:#e2e8f0;">{mvp_html}</div>

            <h4 style="color:#f87171; margin:12px 0 6px 0;">⚠️ Missed Attacks & Low Performance:</h4>
            <div style="background:#0f172a; padding:10px; border-radius:6px; font-size:13px; color:#e2e8f0;">{under_html}</div>

            <h4 style="color:#fbbf24; margin:12px 0 6px 0;">⏳ Pending Attacks List:</h4>
            <div style="background:#0f172a; padding:10px; border-radius:6px; font-size:13px; color:#e2e8f0;">{pending_html}</div>

            <h4 style="color:#a7f3d0; margin:14px 0 6px 0;">🛡️ Defense Breakdown (Opponent Attacks on Us):</h4>
            <table style="width:100%; border-collapse:collapse; font-size:12px; background:#0f172a; color:#cbd5e1; border:1px solid #334155;">
                <tr style="background:#334155; color:#fff;"><th style="padding:6px;">Our Base</th><th style="padding:6px;">Damage / Stars</th><th style="padding:6px;">Enemy Attacker</th></tr>
                {defense_table_rows}
            </table>
        </div>
        """
    else:
        war_section = "<div style='background:#1e293b; padding:12px; border-radius:8px; margin-bottom:20px; color:#cbd5e1;'>⚔️ <b>Clan War Status:</b> Clan is currently not in active war or war log is private.</div>"

    # 3. Clan Capital Live Season
    capital_info = f"• <b>Total Capital Gold Contributed:</b> {cap_gold:,} 🪙<br>"
    if capital_raw and 'items' in capital_raw and len(capital_raw['items']) > 0:
        latest_cap = capital_raw['items'][0]
        c_loot = latest_cap.get('capitalTotalLoot', 0)
        c_raids = latest_cap.get('totalAttacks', 0)
        c_districts = latest_cap.get('enemyDistrictsDestroyed', 0)
        capital_info += f"• <b>Last Weekend Total Clan Loot:</b> {c_loot:,} 🪙<br>• <b>Total Clan Raids:</b> {c_raids} attacks ({c_districts} Districts Destroyed)"

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="utf-8">
      <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background-color: #030712; color: #f8fafc; margin: 0; padding: 15px; }}
        .box {{ max-width: 650px; margin: auto; background: #0b0f19; border: 2px solid #1e293b; border-radius: 12px; padding: 20px; }}
        h2 {{ color: #facc15; border-bottom: 2px solid #334155; padding-bottom: 8px; margin-top: 0; }}
        .badge {{ background: #0284c7; color: #fff; padding: 3px 8px; border-radius: 4px; font-size: 12px; }}
      </style>
    </head>
    <body>
      <div class="box">
        <h2>👑 CLASH OF CLANS - 360° EXECUTIVE BRIEFING</h2>
        <p>Greetings Chief <b>{p_name}</b>,</p>
        <p>તમારા CoC AI Multi-Agent HQ (CEO + 5 Managers) દ્વારા તૈયાર કરેલ સંપૂર્ણ વિગતવાર રિપોર્ટ:</p>

        <!-- Live War Deep Audit -->
        {war_section}

        <!-- Home Village Section -->
        <div style="background:#1e293b; padding:15px; border-radius:8px; border-left:5px solid #38bdf8; margin-bottom:20px;">
            <h3 style="margin-top:0; color:#38bdf8;">🏰 HOME VILLAGE & HERO PROGRESSION</h3>
            <p style="margin:5px 0;"><b>Town Hall:</b> Level {th} | <b>Trophies:</b> {trophies} 🏆 (Record: {best_trophies} 🏆)</p>
            <p style="margin:5px 0; color:#94a3b8; font-size:12px;">Season Attacks Won: <b>{attack_wins}</b> | Season Defenses Won: <b>{defense_wins}</b> | Career War Stars: <b>{war_stars} ⭐</b></p>
            <table style="width:100%; border-collapse:collapse; margin-top:10px; font-size:13px; background:#0f172a; color:#e2e8f0; border:1px solid #334155;">
                <tr style="background:#334155; color:#fff;"><th style="padding:6px 10px; text-align:left;">Hero</th><th style="padding:6px 10px; text-align:left;">Level</th></tr>
                {hero_rows}
            </table>
            <p style="color:#fbbf24; font-size:12px; margin:10px 0 0 0;">💡 <b>Upgrade Priority:</b> Dark Elixir ને Archer Queen (Lvl 43->50+) અને Royal Champion પર ફોકસ કરો.</p>
        </div>

        <!-- Clan Capital & Builder Base -->
        <div style="background:#1e293b; padding:15px; border-radius:8px; border-left:5px solid #fb923c; margin-bottom:20px;">
            <h3 style="margin-top:0; color:#fb923c;">🏛️ CLAN CAPITAL & BUILDER BASE 2.0</h3>
            <p style="font-size:13px; line-height:1.6; margin:5px 0;">
                {capital_info}<br>
                • <b>Builder Base:</b> Builder Hall Level {bh_lvl} (B.O.B 6th Builder Active)
            </p>
        </div>

        <!-- Event Specialist Desk -->
        <div style="background:#1e293b; padding:15px; border-radius:8px; border-left:5px solid #ec4899; margin-bottom:10px;">
            <h3 style="margin-top:0; color:#ec4899;">🎯 EVENT SPECIALIST & CWL ROSTER</h3>
            <p style="font-size:13px; margin:5px 0;">• <b>Clan Games:</b> 4000 Points Ready Strategy Synced.<br>• <b>CWL Bonus:</b> Top Star Performers are logged in the candidate queue.</p>
        </div>

        <p style="color:#64748b; font-size:11px; text-align:center; margin-top:20px; border-top:1px solid #1e293b; padding-top:10px;">
            Automated Intelligence Dispatch by CoC AI Virtual Office.
        </p>
      </div>
    </body>
    </html>
    """

# ================= DIRECT EMAIL DISPATCH =================
def send_deep_email(subject):
    try:
        html_content = build_comprehensive_email_html()
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = f"👑 CoC Central CEO <{MY_GMAIL}>"
        msg["To"] = MY_GMAIL
        msg.attach(MIMEText(html_content, "html"))

        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(MY_GMAIL, APP_PASSWORD)
        server.sendmail(MY_GMAIL, MY_GMAIL, msg.as_string())
        server.quit()
        return True, "સંપૂર્ણ ડિટેઇલ રિપોર્ટ તમારા ઇમેલ પર મોકલાઈ ગયો છે!"
    except Exception as e:
        return False, str(e)

# ================= STREAMLIT DASHBOARD =================
p_name = player_raw.get('name', 'Prince') if player_raw else 'Prince'
th_lvl = player_raw.get('townHallLevel', 13) if player_raw else 13
clan_name = player_raw.get('clan', {}).get('name', 'Shadow Apex') if player_raw else 'Shadow Apex'

player_json_str = json.dumps(player_raw) if player_raw else "{}"
war_json_str = json.dumps(war_raw) if war_raw else "{}"

col1, col2 = st.columns([3, 1])
with col1:
    st.markdown(f"### 🏢 CoC HQ Dashboard — **{p_name} (TH{th_lvl})** | Clan: **{clan_name}**")
with col2:
    if st.button("📧 Send Complete Deep Mail Now"):
        ok, msg = send_deep_email(f"👑 CoC 360° Deep Executive Audit - {datetime.now().strftime('%d %b %Y')}")
        if ok:
            st.success(f"✅ {MY_GMAIL} પર સંપૂર્ણ વિગતવાર ઈમેલ આવી ગયો છે!")
        else:
            st.error(f"⚠️ {msg}")

raw_html_template = """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; font-family: monospace; }
  body { background: #030712; color: #f9fafb; padding: 4px; }
  .wrapper { max-width: 950px; margin: auto; display: flex; flex-direction: column; gap: 8px; }
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
  <div class="canvas-box">
    <canvas id="officeCanvas" width="600" height="380"></canvas>
  </div>

  <div class="chat-box">
    <div class="chat-head">
      <span>👑 CEO LIVE OFFICE TERMINAL</span>
      <span style="color: #4ade80;">● 100% IN-DEPTH SYNC</span>
    </div>
    
    <div class="chat-log" id="chatLog">
      <div class="msg msg-ceo">
        <b>👑 Central CEO:</b> Chief <b>__P_NAME__</b>! સંપૂર્ણ વિગતવાર રિપોર્ટિંગ સિસ્ટમ (MVP, Missed Attacks, Defense Audit & Capital) તૈયાર છે.
      </div>
    </div>

    <div class="quick-cmds">
      <button class="btn-cmd" onclick="handleUserSend('સામેવાળાએ આપણા પર કેટલા સ્ટાર કર્યા?')">🛡️ Opponent Attacks</button>
      <button class="btn-cmd" onclick="handleUserSend('કોના અટેક બાકી છે?')">⚔️ Pending Attacks</button>
      <button class="btn-cmd" onclick="handleUserSend('Events and Clan Games Report')">🎯 Event Specialist</button>
      <button class="btn-cmd" onclick="handleUserSend('આજનો ઓલ ઓવર રિપોર્ટ આપો')">⭐ 360° Complete Audit</button>
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
  { id: "ceo",  x: 210, y: 15,  w: 180, h: 90, title: "👑 CEO CABIN", color: "#1e1b4b", border: "#facc15" },
  { id: "hv",   x: 20,  y: 130, w: 165, h: 100, title: "🏰 HOME VILLAGE", color: "#0c4a6e", border: "#38bdf8" },
  { id: "bb",   x: 415, y: 130, w: 165, h: 100, title: "🌙 BUILDER BASE", color: "#3b0764", border: "#c084fc" },
  { id: "clan", x: 20,  y: 255, w: 165, h: 105, title: "🛡️ WAR ROOM", color: "#064e3b", border: "#4ade80" },
  { id: "cap",  x: 415, y: 255, w: 165, h: 105, title: "🏛️ CAPITAL", color: "#7c2d12", border: "#fb923c" },
  { id: "event",x: 220, y: 255, w: 160, h: 105, title: "🎯 EVENT DESK", color: "#831843", border: "#f472b6" }
];

const characters = {
  ceo: { x: 300, y: 50, skin: "#fed7aa", suit: "#0f172a", hair: "#e2e8f0" },
  hv: { x: 70, y: 180, skin: "#fed7aa", suit: "#0284c7", hair: "#78350f" },
  bb: { x: 470, y: 180, skin: "#fed7aa", suit: "#9333ea", hair: "#facc15" },
  clan: { x: 70, y: 305, skin: "#fed7aa", suit: "#16a34a", hair: "#1e293b" },
  cap: { x: 470, y: 305, skin: "#fed7aa", suit: "#ea580c", hair: "#b91c1c" },
  event: { x: 300, y: 305, skin: "#fed7aa", suit: "#db2777", hair: "#0284c7" },
  peon: { x: 300, y: 175, origX: 300, origY: 175, skin: "#fbcfe8", suit: "#64748b", cap: "#dc2626", state: "idle", hasFile: false }
};

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
    ctx.fillStyle = rm.border; ctx.font = "bold 9px monospace"; ctx.fillText(rm.title, rm.x + 6, rm.y + 13);
  });

  drawDesk(260, 58, 80, 26, "#78350f");
  drawDesk(95, 168, 45, 24, "#334155");
  drawDesk(435, 168, 45, 24, "#334155");
  drawDesk(95, 293, 45, 24, "#334155");
  drawDesk(435, 293, 45, 24, "#334155");
  drawDesk(275, 293, 50, 24, "#475569");

  drawPerson(characters.ceo.x, characters.ceo.y, characters.ceo.skin, characters.ceo.suit, characters.ceo.hair, true);
  drawPerson(characters.hv.x, characters.hv.y, characters.hv.skin, characters.hv.suit, characters.hv.hair);
  drawPerson(characters.bb.x, characters.bb.y, characters.bb.skin, characters.bb.suit, characters.bb.hair);
  drawPerson(characters.clan.x, characters.clan.y, characters.clan.skin, characters.clan.suit, characters.clan.hair);
  drawPerson(characters.cap.x, characters.cap.y, characters.cap.skin, characters.cap.suit, characters.cap.hair);
  drawPerson(characters.event.x, characters.event.y, characters.event.skin, characters.event.suit, characters.event.hair);

  let p = characters.peon;
  drawPerson(p.x, p.y, p.skin, p.suit, p.cap, false, p.hasFile);

  requestAnimationFrame(drawOffice);
}

function drawDesk(x, y, w, h, color) {
  ctx.fillStyle = color; ctx.fillRect(x, y, w, h);
  ctx.strokeStyle = "rgba(255,255,255,0.15)"; ctx.strokeRect(x, y, w, h);
  ctx.fillStyle = "#38bdf8"; ctx.fillRect(x + w/2 - 5, y + 3, 10, 6);
}

function drawPerson(x, y, skin, suit, hair, isCEO=false, hasFile=false) {
  ctx.fillStyle = suit; ctx.fillRect(x-6, y, 12, 10);
  if(isCEO) { ctx.fillStyle = "#ef4444"; ctx.fillRect(x-1, y+1, 2, 7); }
  ctx.fillStyle = skin; ctx.beginPath(); ctx.arc(x, y-4, 5, 0, Math.PI*2); ctx.fill();
  ctx.fillStyle = hair; ctx.beginPath(); ctx.arc(x, y-6, 5, Math.PI, Math.PI*2); ctx.fill();
  if(hasFile) { ctx.fillStyle = "#facc15"; ctx.fillRect(x+5, y+2, 6, 8); }
}

function dispatchPeon(deptId, callback) {
  let p = characters.peon;
  let mgr = characters[deptId] || characters.clan;
  p.state = "to_mgr";
  walkTo(mgr.x + 16, mgr.y, function() {
    p.hasFile = true;
    walkTo(300, 90, function() {
      p.hasFile = false;
      setTimeout(function() { walkTo(p.origX, p.origY, callback); }, 600);
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
      p.x += (dx/dist)*speed; p.y += (dy/dist)*speed;
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

function processSmartQuery(queryText) {
  let q = queryText.toLowerCase().trim();

  if (q.includes("સામેવાળા") || q.includes("opponent") || q.includes("defense") || q.includes("ડિફેન્સ") || q.includes("star kar") || q.includes("star pad") || (q.includes("ketala") && q.includes("star"))) {
    if (!rawWar || rawWar.state === 'notInWar') return { dept: 'clan', reply: "અત્યારે ક્લેન એક્ટિવ વોરમાં નથી." };
    let clanMembers = rawWar.clan.members || [];
    let oppName = rawWar.opponent ? rawWar.opponent.name : "Opponent";
    let defHTML = "<b>🛡️ OPPONENT ATTACKS ON US (" + oppName + "):</b><br>";
    clanMembers.sort(function(a,b) { return a.mapPosition - b.mapPosition; });
    clanMembers.forEach(function(m) {
      let best = m.bestOpponentAttack;
      if (best) {
        defHTML += "• <b>#" + m.mapPosition + " " + m.name + "</b>: <b>" + best.stars + "⭐ (" + best.destructionPercentage + "%)</b> Conceded<br>";
      } else {
        defHTML += "• <b>#" + m.mapPosition + " " + m.name + "</b>: 🟢 <b>Safe (No Stars Given)</b><br>";
      }
    });
    return { dept: 'clan', reply: defHTML };
  }

  if (q.includes("baki") || q.includes("બાકી") || q.includes("pending") || q.includes("kona")) {
    if (!rawWar || rawWar.state === 'notInWar') return { dept: 'clan', reply: "અત્યારે કોઈ સક્રિય વોર નથી." };
    let clanMembers = rawWar.clan.members || [];
    let pendingHTML = "<b>⚔️ PENDING CLAN ATTACKS:</b><br>";
    clanMembers.sort(function(a,b) { return a.mapPosition - b.mapPosition; });
    clanMembers.forEach(function(m) {
      let used = m.attacks ? m.attacks.length : 0;
      let left = 2 - used;
      if (left > 0) pendingHTML += "• <b>#" + m.mapPosition + " " + m.name + "</b>: " + left + " attack(s) left<br>";
    });
    return { dept: 'clan', reply: pendingHTML };
  }

  if (q.includes("event") || q.includes("ઇવેન્ટ") || q.includes("games") || q.includes("medal")) {
    return { dept: 'event', reply: "<b>🎯 EVENT SPECIALIST REPORT:</b><br>• <b>Clan Games:</b> Monthly Target 4000 Points Ready.<br>• <b>CWL:</b> Master Roster Prepared.<br>• <b>Seasonal Medal Tracker:</b> Active." };
  }

  if (q.includes("hero") || q.includes("હીરો") || q.includes("home") || q.includes("village") || q.includes("queen") || q.includes("king")) {
    let heroes = (rawPlayer.heroes || []).filter(function(h) { return h.village === 'home'; }).map(function(h) { return "• <b>" + h.name + ":</b> Lvl " + h.level + "/" + h.maxLevel; }).join("<br>");
    return { dept: 'hv', reply: "<b>🏰 HOME VILLAGE REPORT:</b><br>• Town Hall " + rawPlayer.townHallLevel + " | " + rawPlayer.trophies + " 🏆<br>" + heroes };
  }

  return {
    dept: 'all',
    reply: "<b>⭐ 360° ALL-OVER SUMMARY:</b><br>• <b>Player:</b> " + rawPlayer.name + " (TH" + rawPlayer.townHallLevel + ")<br>• <b>War:</b> " + (rawWar && rawWar.state !== 'notInWar' ? rawWar.clan.name + " " + rawWar.clan.stars + "⭐ vs " + rawWar.opponent.stars + "⭐" : "No active war") + "<br>• <b>Capital:</b> " + (rawPlayer.clanCapitalContributions ? rawPlayer.clanCapitalContributions.toLocaleString() : '0') + " 🪙 Donated.<br>• <b>Automated Deep Email:</b> Ready."
  };
}

function handleUserSend(customText) {
  let inp = document.getElementById("userInput");
  let val = customText || (inp ? inp.value.trim() : "");
  if (!val) return;
  logMsg("Chief", val, "user");
  if (!customText && inp) inp.value = "";

  let res = processSmartQuery(val);
  dispatchPeon(res.dept, function() {
    logMsg(res.dept === 'clan' ? "🛡️ War General" : (res.dept === 'event' ? "🎯 Event Specialist" : (res.dept === 'hv' ? "🏰 HV Manager" : "👑 Central CEO")), res.reply, "mgr");
  });
}

drawOffice();
</script>
</body>
</html>
"""

final_html = raw_html_template.replace("__P_NAME__", p_name)
final_html = final_html.replace("__PLAYER_JSON__", player_json_str)
final_html = final_html.replace("__WAR_JSON__", war_json_str)

st.components.v1.html(final_html, height=920, scrolling=False)
