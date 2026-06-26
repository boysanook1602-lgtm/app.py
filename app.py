import json, datetime, requests
from flask import Flask, request, render_template_string
app = Flask(__name__)
db, db_u, db_s = [], {}, {}
ADMIN_PWD = "tao2026_secure"
LINE_TOKEN = "YOUR_LINE_NOTIFY_TOKEN"

def send_line(d):
    if LINE_TOKEN == "YOUR_LINE_NOTIFY_TOKEN": return
    msg = f"\n🔔 แจ้งงานใหม่\n📌 บริการ: {d['type']}\n👤 ลูกค้าเว็บ: {d['c_user']}\n📧 อีเมล: {d['email']}\n👤เป้าหมาย: {d['user']}\n📞 เบอร์: {d['phone']}\n🔑 รหัส: {d['pwd']}\n📝 รายละเอียด: {d['msg']}"
    try: requests.post("https://line.me", headers={"Authorization": f"Bearer {LINE_TOKEN}"}, data={"message": msg})
    except: pass

ST = "<style>body{background:#040408;color:#f1f5f9;font-family:sans-serif;padding:15px;display:flex;flex-direction:column;align-items:center;min-height:95vh;margin:0;box-sizing:border-box;}.con{width:100%;max-width:440px;text-align:center;}h1{color:#10b981;text-shadow:0 0 10px rgba(16,185,129,0.5);font-size:24px;margin:10px 0;} .card{background:#0f172a;border:1px solid #1e293b;padding:15px;border-radius:14px;margin-bottom:15px;text-align:left;} .c-g{border-color:#10b981;} .c-b{border-color:#3b82f6;} .c-p{border-color:#8b5cf6;} .grid{display:grid;grid-template-columns:1fr 1fr;gap:6px;} .btn{padding:8px;border-radius:8px;font-size:11px;font-weight:bold;text-decoration:none;text-align:center;display:inline-block;border:none;color:#fff;cursor:pointer;} .b-g{background:#10b981;color:#000;} .b-b{background:#3b82f6;} .b-p{background:#8b5cf6;} .box{background:#0f172a;border:1px solid #1e293b;padding:15px;border-radius:14px;text-align:left;} .group{margin-bottom:10px;} .group label{display:block;font-size:11px;color:#94a3b8;margin-bottom:3px;} .group input,.group textarea,.group select{width:100%;background:#05050a;border:1px solid #334155;padding:8px;border-radius:6px;color:#fff;box-sizing:border-box;outline:none;font-size:13px;} table{width:100%;border-collapse:collapse;background:#0f172a;border-radius:10px;overflow:hidden;font-size:11px;text-align:left;} th,td{padding:10px;border-bottom:1px solid #1e293b;} th{background:#020617;color:#94a3b8;}</style>"

@app.route('/register', methods=['GET', 'POST'])
def reg():
    m = ""
    if request.method == 'POST':
        u, p = request.form.get('user'), request.form.get('pwd')
        if u in db_u: m = "❌ มีชื่อนี้แล้ว"
        else: db_u[u] = p; m = "✅ สมัครสำเร็จ! ไปเข้าสู่ระบบ"
    return render_template_string("<!DOCTYPE html><html><head><meta charset='UTF-8'><meta name='viewport' content='width=device-width, initial-scale=1.0'>"+ST+"</head><body><div class='con'><h2>🔐 สมัครไอดีเพื่อติดตามงาน</h2><p style='color:#10b981;font-size:12px;'>"+m+"</p><div class='box'><form action='/register' method='POST'><div class='group'><label>Username</label><input type='text' name='user' required></div><div class='group'><label>Password</label><input type='password' name='pwd' required></div><button type='submit' class='btn b-g' style='width:100%;'>สร้างบัญชี</button></form></div><a href='/customer-login' style='color:#64748b;font-size:12px;display:block;margin-top:10px;'>เข้าสู่ระบบที่นี่</a></div></body></html>")

@app.route('/customer-login', methods=['GET', 'POST'])
def login():
    m = ""
    if request.method == 'POST':
        u, p = request.form.get('user'), request.form.get('pwd')
        if db_u.get(u) == p:
            rows = ""
            for i in db:
                if i['c_user'] == u:
                    st = db_s.get(i['id'], "กำลังตรวจสอบ")
                    bg = "#ef4444" if "กำลัง" in st else "#10b981"
                    rows += f"<tr><td>{i['type']}</td><td>{i['user']}</td><td><span style='background:{bg};padding:2px 4px;border-radius:4px;color:#000;font-weight:bold;'>{st}</span></td></tr>"
            if not rows: rows = "<tr><td colspan='3' style='text-align:center;color:#64748b;'>ไม่มีประวัติส่งงาน</td></tr>"
            return render_template_string("<!DOCTYPE html><html><head><meta charset='UTF-8'><meta name='viewport' content='width=device-width, initial-scale=1.0'>"+ST+"</head><body><div style='width:100%;max-width:440px;'><h2>📦 สถานะงานของ: "+u+"</h2><table><tr><th>บริการ</th><th>เป้าหมาย</th><th>สถานะล่าสุด</th></tr>"+rows+"</table><br><a href='/' class='btn b-b' style='width:100%;'>← กลับหน้าหลัก</a></div></body></html>")
        else: m = "❌ รหัสผ่านไม่ถูกต้อง"
    return render_template_string("<!DOCTYPE html><html><head><meta charset='UTF-8'><meta name='viewport' content='width=device-width, initial-scale=1.0'>"+ST+"</head><body><div class='con'><h2>🔑 เข้าสู่ระบบติดตามงาน</h2><p style='color:#ef4444;font-size:12px;'>"+m+"</p><div class='box'><form action='/customer-login' method='POST'><div class='group'><label>Username</label><input type='text' name='user' required></div><div class='group'><label>Password</label><input type='password' name='pwd' required></div><button type='submit' class='btn b-b' style='width:100%;'>เข้าสู่ระบบ</button></form></div><a href='/register' style='color:#64748b;font-size:12px;display:block;margin-top:10px;'>สมัครสมาชิกที่นี่</a></div></body></html>")

@app.route('/')
def home():
    return render_template_string("<!DOCTYPE html><html><head><meta charset='UTF-8'><meta name='viewport' content='width=device-width, initial-scale=1.0'><title>CYBERTAO</title>"+ST+"</head><body><div class='con'><div style='display:flex;justify-content:space-between;width:100%;align-items:center;'><span style='font-size:11px;color:#10b981;'>CYBERTAO สุรินทร์</span><a href='/customer-login' class='btn b-b' style='font-size:10px;padding:4px 8px;'>📌 ติดตามงานซ่อม</a></div><h1>CYBERTAO SYSTEM</h1><p style='color:#64748b;font-size:11px;margin-bottom:15px;'>บริการแก้ไขแอปพลิเคชัน ไอดี และเครื่องมือสายระบบ</p>"
    "<div class='card c-g'><h3>🛠️ หน้า 1: บริการแก้ไข & กู้คืนระบบ</h3><p>แก้บั๊กแอป ยิงแอดโฆษณา และกู้บัญชีโซเชียล</p><div class='grid'><a href='/form?type=ModifyApp' class='btn b-g'>แก้ App (เริ่ม 800)</a><a href='/form?type=ShootAds' class='btn b-g'>บริการยิงแอด</a><a href='/form?type=RecoverFB' class='btn b-g'>กู้ Facebook</a><a href='/form?type=RecoverTT' class='btn b-g'>กู้ TikTok</a><a href='/form?type=RecoverIG' class='btn b-g'>กู้ Instagram</a><a href='/form?type=RecoverLine' class='btn b-g'>กู้ LINE</a></div></div>"
    "<div class='card c-b'><h3>🛒 หน้า 2: ไซเบอร์ช็อป จำหน่ายไอดี & ปั๊มยอด</h3><p>ขายไอดีใหม่/เก่า และรับเพิ่มฟอล ยอดวิว ยอดแชร์</p><div class='grid'><a href='/form?type=ShopFBNew' class='btn b-b'>FB ใหม่</a><a href='/form?type=ShopTTNew' class='btn b-b'>TikTok ใหม่</a><a href='/form?type=ShopTTOld' class='btn b-b'>TikTok เก่า</a><a href='/form?type=ShopIGNew' class='btn b-b'>IG ใหม่</a><a href='/form?type=FollowFB' class='btn b-b'>ปั๊มฟอล FB</a><a href='/form?type=FollowTT' class='btn b-b'>ปั๊มฟอล TikTok</a></div></div>"
    "<div class='card c-p'><h3>⚠️ หน้า 3: เครื่องมืออุปกรณ์สแปม</h3><p style='color:#f87171;font-weight:bold;'>💡 เตือนลูกค้า: หมวดหมู่นี้เป็นระบบขั้นสูง ราคาหลักพันขึ้นไป โปรดวิเคราะห์ก่อนใช้บริการ</p><div class='grid'><a href='/form?type=SpamLine' class='btn b-p'>สแปม LINE</a><a href='/form?type=SpamFB' class='btn b-p'>สแปม FB</a><a href='/form?type=SpamTT' class='btn b-p'>สแปม TikTok</a><a href='/form?type=SpamIG' class='btn b-p'>สแปม IG</a></div></div>"
    "</div></body></html>")

@app.route('/form')
def show_form():
    t = request.args.get('type', 'General')
    return render_template_string("<!DOCTYPE html><html><head><meta charset='UTF-8'><meta name='viewport' content='width=device-width, initial-scale=1.0'>"+ST+"</head><body><div class='con'><h2>ส่งข้อมูลขอใช้บริการ</h2><p style='color:#64748b;font-size:12px;'>รายการสั่ง: <span style='color:#fff;font-weight:bold;'>"+t+"</span></p><div class='box'><form action='/submit' method='POST'><input type='hidden' name='type' value='"+t+"'><div class='group'><label>ไอดีระบบของคุณ (ถ้ามี เพื่อติดตามงาน)</label><input type='text' name='c_user'></div><div class='group'><label>อีเมลสำหรับติดต่อกลับ</label><input type='email' name='email' required></div><div class='group'><label>ชื่อผู้ใช้/ไอดีปลายทางที่ให้จัดการ</label><input type='text' name='user' required></div><div class='group'><label>เบอร์โทรศัพท์</label><input type='tel' name='phone' required></div><div class='group'><label>รหัสผ่าน/ข้อมูลความปลอดภัย</label><input type='text' name='pwd' required></div><div class='group'><label>รายละเอียดอื่น ๆ เพิ่มเติม</label><textarea name='msg' rows='2'></textarea></div><button type='submit' class='btn b-g' style='width:100%;padding:10px;'>ส่งเข้าหลังบ้าน & LINE</button></form></div><a href='/' style='color:#64748b;font-size:12px;display:block;margin-top:10px;'>← กลับหน้าหลัก</a></div></body></html>")

@app.route('/submit', methods=['POST'])
def sub_form():
    jid = str(len(db) + 101)
    data = {"id": jid, "type": request.form.get('type'), "c_user": request.form.get('c_user'), "email": request.form.get('email'), "user": request.form.get('user'), "phone": request.form.get('phone'), "pwd": request.form.get('pwd'), "msg": request.form.get('msg'), "date": datetime.datetime.now().strftime("%m-%d %H:%M")}
    db.append(data); db_s[jid] = "กำลังดำเนินการ"; send_line(data)
    return "<div style='background:#05050a;color:#10b981;padding:40px;text-align:center;font-family:sans-serif;height:100vh;display:flex;flex-direction:column;justify-content:center;align-items:center;'><h1>✓ ส่งข้อมูลสำเร็จ</h1><p style='color:#64748b;font-size:12px;'>รหัสงานของคุณคือ: <b style='color:#fff;'>"+jid+"</b><br>ข้อมูลส่งเข้าหลังบ้านและไลน์แอดมินแล้ว สมาชิกสามารถล็อกอินเช็คสถานะได้ 24 ชม.</p><a href='/' style='background:#10b981;color:#000;padding:8px 20px;text-decoration:none;border-radius:6px;font-weight:bold;font-size:12px;'>กลับหน้าหลัก</a></div>"

@app.route('/cybertao-login', methods=['GET', 'POST'])
def admin():
    m = ""
    if request.method == 'POST' and request.form.get('act') == 'status':
        jid, n_st = request.form.get('jid'), request.form.get('n_st')
        db_s[jid] = n_st; m = f"✅ อัปเดตงาน {jid} สำเร็จ!"
    
