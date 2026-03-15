from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3
import random
import smtplib
from email.message import EmailMessage

app = FastAPI()

# تفعيل الاتصال للمتصفحات
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_NAME = "mart.db"
otp_store = {}

# --- إعدادات "محرك الإرسال" (إيميل المنصة) ---
# ملاحظة: هذا الإيميل هو الذي سيظهر للمستخدمين كمرسل (اسم المنصة)
ADMIN_EMAIL = "manqiyah@gmail.com"  
ADMIN_PASSWORD = "qxsm hpvm kaij ntwz" # كود الـ 16 حرفاً من جوجل

class OTPVerify(BaseModel):
    national_id: str
    code: str

@app.get("/send-otp/{national_id}")
def send_otp(national_id: str):
    with sqlite3.connect(DB_NAME) as con:
        cur = con.cursor()
        # هنا نبحث عن إيميل الشخص الذي أدخل هويته
        cur.execute("SELECT email FROM profile WHERE national_id=?", (national_id,))
        row = cur.fetchone()
        
        if not row:
            return {"success": False, "message": "رقم الهوية غير مسجل"}

        user_dest_email = row[0] # هذا إيميل المستخدم (المستلم)
        otp = str(random.randint(1000, 9999))
        otp_store[national_id] = otp

        try:
            msg = EmailMessage()
            msg.set_content(f"مرحباً بك في منصة منقية\n\nرمز التحقق الخاص بك هو: {otp}")
            msg['Subject'] = 'رمز التحقق - منقية'
            msg['From'] = ADMIN_EMAIL
            msg['To'] = user_dest_email # الإرسال يتم للمستخدم صاحب الهوية

            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(ADMIN_EMAIL, ADMIN_PASSWORD)
                smtp.send_message(msg)
            
            return {"success": True, "message": f"تم إرسال الرمز إلى {user_dest_email[:3]}***"}
        except Exception as e:
            return {"success": False, "message": "خطأ في مزود خدمة الإيميل"}

@app.post("/verify-otp")
def verify_otp(data: OTPVerify):
    if otp_store.get(data.national_id) == data.code:
        return {"success": True}
    return {"success": False, "message": "الرمز غير صحيح"}

@app.get("/get-user/{national_id}")
def get_user(national_id: str):
    with sqlite3.connect(DB_NAME) as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("SELECT full_name, university, skills FROM profile WHERE national_id=?", (national_id,))
        row = cur.fetchone()
        if row:
            return {"success": True, "data": dict(row)}
        return {"success": False}