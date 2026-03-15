import streamlit as st 
import datetime
import sqlite3
import pandas as pd
import io


# الداتابيس   
DB_NAME = "mart.db"

def create_table():
    with sqlite3.connect(DB_NAME) as con:
        con.execute("""
        CREATE TABLE IF NOT EXISTS profile(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT, national_id TEXT, birth_date TEXT, 
            phone TEXT, email TEXT, university TEXT, 
            degree TEXT, experience_years INTEGER, 
            skills TEXT, language TEXT
        )
        """)

def insert_local(name, id_v, birth, phone, mail, uni, deg, exp, sk, lang):
    with sqlite3.connect(DB_NAME) as con:
        con.execute("""
        INSERT INTO profile (full_name, national_id, birth_date, phone, email, university, degree, experience_years, skills, language)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (name, id_v, str(birth), phone, mail, uni, deg, exp, ", ".join(sk), ", ".join(lang)))

create_table()

# الواجهة  
st.set_page_config(page_title="منصة الكفاءات الوطنية", layout="wide")
st.title(" منصة تسجيل بيانات المستخدمين")
st.info("سجل بياناتك الآن لتنضم إلى نخبة الكفاءات في المملكة")

# استمارة التسجيل 

c1, c2 = st.columns(2)
with c1:
    name = st.text_input("👤 الاسم الرباعي الكامل")
with c2:
    id_val = st.text_input("🆔 رقم الهوية أو الإقامة", max_chars=10)

c3, c4 = st.columns(2)
with c3:
    phone = st.text_input("📱 رقم الجوال", placeholder="05XXXXXXXX", max_chars=10)
with c4:
    email = st.text_input("📧 البريد الإلكتروني")

c5, c6 = st.columns(2)
with c5:
    birth = st.date_input("📅 تاريخ الميلاد", value=datetime.date(2000, 1, 1), 
                          min_value=datetime.date(1920, 1, 1), max_value=datetime.date.today())
with c6:
    uni = st.selectbox("🎓 الجامعة", [
        "جامعة الملك فيصل", "جامعة الملك عبدالعزيز", "جامعة الملك سعود", "جامعة الملك فهد للبترول والمعادن", 
        "جامعة الملك عبدالله للعلوم والتقنية", "جامعة أم القرى", "جامعة الإمام عبدالرحمن بن فيصل", "جامعة الملك خالد", 
        "جامعة الأميرة نورة بنت عبدالرحمن", "الجامعة الإسلامية بالمدينة المنورة", "جامعة الإمام محمد بن سعود الإسلامية", 
        "جامعة نايف العربية للعلوم الأمنية", "جامعة القصيم", "جامعة طيبة", "جامعة الطائف", "جامعة حائل", 
        "جامعة جازان", "جامعة الجوف", "جامعة الباحة", "جامعة تبوك", "جامعة نجران", "جامعة الحدود الشمالية", 
        "جامعة الملك سعود بن عبدالعزيز للعلوم الصحية", "جامعة الأمير سطام بن عبدالعزيز", "جامعة شقراء", 
        "جامعة المجمعة", "الجامعة السعودية الإلكترونية", "جامعة جدة", "جامعة بيشة", "كلية المدربين التقنيين", 
        "جامعة حفر الباطن", "كلية الجبيل الصناعية", "كلية ينبع الصناعية", "لايوجد"
    ])

c7, c8 = st.columns(2)
with c7:
    degree = st.selectbox("📜 الدرجة العلمية", [
        "دكتوراه", "ماجستير", "بكالوريوس", "دبلوم عالي", "دبلوم متوسط", "دبلوم", "الثانوية العامة"
    ])
with c8:
    exp = st.number_input("⏳ سنوات الخبرة", min_value=0, max_value=50, step=1)

skills = st.multiselect("🛠️ المهارات", [
    "العمل الجماعي", "حل المشكلات", "التسويق", "إدارة المشاريع", "تحليل البيانات", "البرمجة", 
    "الذكاء العاطفي", "المبادرة", "القيادة والتأثير الاجتماعي", "تحليل الأعمال"
])

lang = st.multiselect("🌐 اللغات", [
    "العربية", "الإنجليزية", "الصينية", "الهندية", "الإسبانية", "الفرنسية"
])
st.markdown("---")

# زر الحفظ 
if st.button("🚀 تسجيل البيانات في النظام", use_container_width=True):
    if len(name.split()) < 4 or len(id_val) != 10 or not phone.startswith("05") or len(skills) < 1:
        st.error("⚠️ يرجى تعبئة البيانات بشكل صحيح (الاسم رباعي، الهوية 10 أرقام، الجوال يبدأ بـ 05)")
    else:
        insert_local(name, id_val, birth, phone, email, uni, degree, exp, skills, lang)
        st.success("🎉 تم حفظ بياناتك في قاعدة البيانات بنجاح")
        st.balloons()

# لوحة الإدارة 
with st.sidebar:
    st.header("🔑 قسم الإدارة")
    pw = st.text_input("كلمة المرور", type="password")
    
    if pw == "1234":
        st.sidebar.success("أهلاً بك أيها المسؤول")
        
        # جلب البيانات
        with sqlite3.connect(DB_NAME) as con:
            df_admin = pd.read_sql_query("SELECT * FROM profile ORDER BY id DESC", con)
        
        st.write(f"### قائمة المسجلين ({len(df_admin)})")
        st.dataframe(df_admin)

        # التنظيف
        st.markdown("---")
        st.warning("انتبه من زر حذف البيانات!")
        if st.button("🗑️ حذف جميع البيانات"):
            with sqlite3.connect(DB_NAME) as con:
                cursor = con.cursor()
                cursor.execute("DELETE FROM profile") 
                con.commit()
            st.rerun() 
        
        # الإكسل 
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df_admin.to_excel(writer, index=False)
        st.download_button("📥 تحميل Excel", data=output.getvalue(), file_name="kfaat_export.xlsx")





