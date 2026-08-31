import urllib.request
import urllib.parse
import json
import smtplib
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime

PLAYER_TAG = "#GVQPR9J82"
SUPERCELL_API_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6ImM0MDk0Nzk4LTViODktNDIxZC1hYzcwLThjY2ViOGZjMTFjYiIsImlhdCI6MTc4ODA3OTAwNywic3ViIjoiZGV2ZWxvcGVyLzllYmFiYzlmLTM0M2UtNDU2My1iYmM0LTAyOGJjZWE1MTEzMyIsInNjb3BlcyI6WyJjbGFzaCJdLCJsaW1pdHMiOlt7InRpZXIiOiJkZXZlbG9wZXIvc2lsdmVyIiwidHlwZSI6InRocm90dGxpbmcifSx7ImNpZHJzIjpbIjM1LjIzMC41Ni4zMCJdLCJ0eXBlIjoiY2xpZW50In1dfQ._wLkYrhFvkLu4mcFpOdo5zzcTA0sXdxFrFd_wRi5SSBZJwekszYTENnmXVhoLkB2PYHAfNU7IRgV47YDyaY1dQ"
MY_GMAIL = "viranip71@gmail.com"
APP_PASSWORD = "wdckbdeqnfzoxzfa"

def api_get(endpoint):
    try:
        url = f"https://api.clashofclans.com/v1{endpoint}"
        req = urllib.request.Request(url, headers={"Authorization": f"Bearer {SUPERCELL_API_TOKEN.strip()}", "Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read().decode('utf-8'))
    except Exception as e:
        return None

def send_mail(subject, html_body):
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = f"👑 CoC Central CEO <{MY_GMAIL}>"
        msg["To"] = MY_GMAIL
        msg.attach(MIMEText(html_body, "html"))

        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(MY_GMAIL, APP_PASSWORD)
        server.sendmail(MY_GMAIL, MY_GMAIL, msg.as_string())
        server.quit()
        print(f"✅ Email Sent: {subject}")
        return True
    except Exception as e:
        print(f"❌ Error sending email: {e}")
        return False

# ================= 1. DAILY MORNING 7:30 AM REPORT =================
def send_daily_report():
    clean_tag = urllib.parse.quote(PLAYER_TAG.strip())
    p = api_get(f"/players/{clean_tag}")
    if not p: return

    c_tag = p.get('clan', {}).get('tag')
    war = api_get(f"/clans/{urllib.parse.quote(c_tag)}/currentwar") if c_tag else None

    heroes_html = ""
    for h in p.get('heroes', []):
        if h.get('village') == 'home':
            heroes_html += f"<tr><td style='padding:6px; border:1px solid #334155;'><b>{h['name']}</b></td><td style='padding:6px; border:1px solid #334155; color:#38bdf8;'>Level {h['level']} / {h.get('maxLevel', '?')}</td></tr>"

    war_html = "Currently not in active war."
    if war and war.get('state') != 'notInWar':
        c = war.get('clan', {})
        o = war.get('opponent', {})
        war_html = f"<b>{c.get('name')} {c.get('stars')}⭐ ({round(c.get('destructionPercentage',0),1)}%)</b> vs <b>{o.get('name')} {o.get('stars')}⭐ ({round(o.get('destructionPercentage',0),1)}%)</b><br>Attacks: {c.get('attacks')}/{war.get('teamSize', 5)*2}"

    body = f"""
    <div style="font-family: Arial, sans-serif; background: #030712; color: #f8fafc; padding: 20px; border-radius: 10px;">
        <h2 style="color: #facc15; border-bottom: 2px solid #334155; padding-bottom: 8px;">👑 CLASH OF CLANS - DAILY 7:30 AM BRIEFING</h2>
        <p>Chief <b>{p.get('name')}</b>,</p>
        
        <h3 style="color: #38bdf8;">🏰 Home Village & Heroes</h3>
        <p><b>Town Hall:</b> Level {p.get('townHallLevel')} | <b>Trophies:</b> {p.get('trophies')} 🏆 | <b>Clan:</b> {p.get('clan', {}).get('name')}</p>
        <table style="width:100%; border-collapse: collapse; background: #1e293b; color: #e2e8f0;">
            {heroes_html}
        </table>

        <h3 style="color: #4ade80; margin-top: 15px;">⚔️ Live Clan War Status</h3>
        <div style="background: #1e293b; padding: 10px; border-radius: 6px;">{war_html}</div>

        <h3 style="color: #fb923c; margin-top: 15px;">🏛️ Clan Capital & Events</h3>
        <p>• <b>Total Capital Gold:</b> {p.get('clanCapitalContributions', 0):,} 🪙<br>• <b>Builder Base:</b> BH{p.get('builderHallLevel', 8)} (B.O.B Active)</p>
    </div>
    """
    send_mail(f"👑 CoC Daily Briefing (7:30 AM) - Chief {p.get('name')}", body)

# ================= 2. WAR END DETAILED POST-MORTEM =================
def send_war_end_report():
    clean_tag = urllib.parse.quote(PLAYER_TAG.strip())
    p = api_get(f"/players/{clean_tag}")
    if not p or 'clan' not in p: return
    c_tag = p['clan'].get('tag')
    war = api_get(f"/clans/{urllib.parse.quote(c_tag)}/currentwar")

    if not war or war.get('state') != 'warEnded':
        return

    c_info = war.get('clan', {})
    o_info = war.get('opponent', {})
    c_stars = c_info.get('stars', 0)
    o_stars = o_info.get('stars', 0)
    c_dest = round(c_info.get('destructionPercentage', 0), 1)
    o_dest = round(o_info.get('destructionPercentage', 0), 1)

    won = c_stars > o_stars or (c_stars == o_stars and c_dest > o_dest)
    result_title = "🏆 VICTORY! ક્લેન વોર જીતી ગયા!" if won else "❌ DEFEAT! વોરમાં હાર થઈ."

    mvp_list = []
    under_list = []
    def_rows = ""

    members = c_info.get('members', [])
    members.sort(key=lambda x: x.get('mapPosition', 99))

    for m in members:
        atts = m.get('attacks', [])
        used = len(atts)
        m_stars = sum([a.get('stars', 0) for a in atts])
        
        # Performance
        if m_stars >= 5 or (used > 0 and m_stars == used * 3):
            mvp_list.append(f"🌟 <b>#{m.get('mapPosition')} {m.get('name')}</b> (TH{m.get('townhallLevel')}): <b>{m_stars}⭐</b> scored ({used}/2 attacks)")
        elif used == 0:
            under_list.append(f"❌ <b>#{m.get('mapPosition')} {m.get('name')}</b>: 0/2 Attacks (Missed Both Attacks!)")
        elif m_stars <= 2 and used == 2:
            under_list.append(f"⚠️ <b>#{m.get('mapPosition')} {m.get('name')}</b>: Only {m_stars}⭐ across 2 attacks")

        # Defense
        best_def = m.get('bestOpponentAttack')
        if best_def:
            def_rows += f"<tr><td style='padding:6px; border:1px solid #334155;'>#{m.get('mapPosition')} <b>{m.get('name')}</b></td><td style='padding:6px; border:1px solid #334155; color:#ef4444;'>{best_def.get('stars')}⭐ ({best_def.get('destructionPercentage')}%)</td></tr>"
        else:
            def_rows += f"<tr><td style='padding:6px; border:1px solid #334155;'>#{m.get('mapPosition')} <b>{m.get('name')}</b></td><td style='padding:6px; border:1px solid #334155; color:#22c55e;'>🟢 100% Safe (0 Stars given)</td></tr>"

    mvp_html = "<br>".join(mvp_list) if mvp_list else "None"
    under_html = "<br>".join(under_list) if under_list else "તમામ પ્લેયર્સે ઉત્તમ પ્રદર્શન કર્યું!"

    body = f"""
    <div style="font-family: Arial, sans-serif; background: #030712; color: #f8fafc; padding: 20px; border-radius: 10px;">
        <h2 style="color: {'#22c55e' if won else '#ef4444'}; border-bottom: 2px solid #334155; padding-bottom: 8px;">{result_title}</h2>
        
        <p style="font-size:16px;">
            <b>{c_info.get('name')}</b> <span style="color:#facc15;"><b>{c_stars}⭐ ({c_dest}%)</b></span> vs 
            <b>{o_info.get('name')}</b> <span style="color:#facc15;"><b>{o_stars}⭐ ({o_dest}%)</b></span>
        </p>

        <h3 style="color: #38bdf8;">🌟 Best Performers (MVPs / Top Attackers):</h3>
        <div style="background: #1e293b; padding: 10px; border-radius: 6px; font-size:13px;">{mvp_html}</div>

        <h3 style="color: #f87171; margin-top:15px;">⚠️ Missed Attacks & Poor Performance:</h3>
        <div style="background: #1e293b; padding: 10px; border-radius: 6px; font-size:13px;">{under_html}</div>

        <h3 style="color: #a7f3d0; margin-top:15px;">🛡️ Defense Audit (સામેવાળાએ આપણા પર કરેલા અટેક્સ):</h3>
        <table style="width:100%; border-collapse: collapse; background: #1e293b; color: #e2e8f0; font-size:12px;">
            <tr style="background:#334155;"><th style="padding:6px;">Our Member</th><th style="padding:6px;">Damage / Stars Conceded</th></tr>
            {def_rows}
        </table>
    </div>
    """
    send_mail(f"⚔️ WAR END REPORT: {c_info.get('name')} ({c_stars}⭐) vs {o_info.get('name')} ({o_stars}⭐)", body)

# ================= 3. CLAN CAPITAL WEEKEND REPORT =================
def send_capital_report():
    clean_tag = urllib.parse.quote(PLAYER_TAG.strip())
    p = api_get(f"/players/{clean_tag}")
    if not p or 'clan' not in p: return
    c_tag = p['clan'].get('tag')
    cap_seasons = api_get(f"/clans/{urllib.parse.quote(c_tag)}/capitalraidseasons?limit=1")

    if not cap_seasons or 'items' not in cap_seasons or len(cap_seasons['items']) == 0:
        return

    latest = cap_seasons['items'][0]
    total_loot = latest.get('capitalTotalLoot', 0)
    total_attacks = latest.get('totalAttacks', 0)
    districts = latest.get('enemyDistrictsDestroyed', 0)

    body = f"""
    <div style="font-family: Arial, sans-serif; background: #030712; color: #f8fafc; padding: 20px; border-radius: 10px;">
        <h2 style="color: #fb923c; border-bottom: 2px solid #334155; padding-bottom: 8px;">🏛️ CLAN CAPITAL RAID WEEKEND COMPLETION REPORT</h2>
        <p>Chief <b>{p.get('name')}</b>, આ વીકેન્ડ રેઇડ્સ પૂર્ણ થઈ ગઈ છે:</p>
        
        <div style="background: #1e293b; padding: 12px; border-radius: 6px; font-size:14px; line-height:1.7;">
            • <b>Total Clan Capital Gold Looted:</b> <span style="color:#facc15;"><b>{total_loot:,} 🪙</b></span><br>
            • <b>Total Clan Attacks Used:</b> {total_attacks} attacks<br>
            • <b>Enemy Districts Destroyed:</b> {districts} Districts<br>
            • <b>Your Total Lifetime Contribution:</b> {p.get('clanCapitalContributions', 0):,} 🪙
        </div>
    </div>
    """
    send_mail(f"🏛️ Clan Capital Raid Weekend Finished - {p.get('clan', {}).get('name')}", body)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        mode = sys.argv[1]
        if mode == "--daily":
            send_daily_report()
        elif mode == "--war":
            send_war_end_report()
        elif mode == "--capital":
            send_capital_report()
        elif mode == "--all":
            send_daily_report()
            send_war_end_report()
            send_capital_report()
    else:
        send_daily_report()
