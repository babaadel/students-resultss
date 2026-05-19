import streamlit as st
import pandas as pd
from fpdf import FPDF
import base64

# 1. إعدادات الصفحة والتنسيق
st.set_page_config(page_title="منصة التميز للنتائج", page_icon="🎓", layout="centered")

st.markdown("""
    <style>
    @import url('https://googleapis.com');
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif; text-align: right; direction: rtl; }
    .main { background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); }
    .stCard { background: white; padding: 25px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); border-top: 5px solid #2563eb; margin-bottom: 20px; }
    .metric-card { background: #f8fafc; padding: 15px; border-radius: 10px; text-align: center; border: 1px solid #e2e8f0; }
    .metric-value { font-size: 24px; font-weight: bold; color: #2563eb; }
    .metric-label { font-size: 14px; color: #64748b; }
    div.stButton > button { width: 100%; border-radius: 12px; background: linear-gradient(90deg, #2563eb, #1e40af); color: white; font-weight: bold; height: 3.5em; border: none; }
    </style>
    """, unsafe_allow_html=True)

# 2. وظيفة إنشاء ملف PDF
def create_pdf(student_data, subjects):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    
    # عنوان الشهادة
    pdf.cell(200, 10, txt="Student Result Report", ln=True, align='C')
    pdf.ln(10)
    
    # معلومات الطالب
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Student Name: {student_data['الاسم']}", ln=True, align='L')
    pdf.cell(200, 10, txt=f"ID: {student_data['الرقم']}", ln=True, align='L')
    pdf.cell(200, 10, txt=f"GPA: {student_data.get('المعدل', 'N/A')}%", ln=True, align='L')
    pdf.cell(200, 10, txt=f"Rank: {student_data.get('الترتيب', 'N/A')}", ln=True, align='L')
    
    pdf.ln(10)
    pdf.cell(200, 10, txt="Subject Details:", ln=True, align='L')
    
    # تفاصيل المواد
    for subj in subjects:
        pdf.cell(200, 10, txt=f"- {subj}: {student_data[subj]}", ln=True, align='L')
    
    return pdf.output(dest='S').encode('latin-1')

# 3. تحميل البيانات
@st.cache_data
def load_data():
    try:
        df = pd.read_excel("data.xlsx")
        if 'المعدل' in df.columns and 'الترتيب' not in df.columns:
            df['الترتيب'] = df['المعدل'].rank(ascending=False, method='min').astype(int)
        return df
    except: return None

df = load_data()

# 4. الواجهة البرمجية
st.markdown("<h1 style='text-align: center; color: #1e40af;'>🎓 منصة استعلام النتائج</h1>", unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="stCard">', unsafe_allow_html=True)
    search_query = st.text_input("بحث بالاسم أو الرقم:", placeholder="اكتب هنا...")
    
    if search_query:
        if df is not None:
            query_str = str(search_query).strip()
            result = df[(df['الرقم'].astype(str) == query_str) | (df['الاسم'].str.contains(query_str, na=False))]
            
            if not result.empty:
                student = result.iloc[0]
                status = student.get('الحالة', 'ناجح')

                if status == "ناجح":
                    st.balloons()
                    st.success(f"🎉 مبارك النجاح! {student['الاسم']}")
                else:
                    st.markdown("<h2 style='text-align: center;'>😔</h2>", unsafe_allow_html=True)
                    st.error(f"حظ أوفر.. {student['الاسم']}")

                # عرض المعدل والترتيب
                c1, c2 = st.columns(2)
                c1.markdown(f'<div class="metric-card"><div class="metric-label">المعدل</div><div class="metric-value">{student.get("المعدل", "N/A")}%</div></div>', unsafe_allow_html=True)
                c2.markdown(f'<div class="metric-card"><div class="metric-label">الترتيب</div><div class="metric-value">{student.get("الترتيب", "N/A")}#</div></div>', unsafe_allow_html=True)

                # زر PDF
                exclude = ['الرقم', 'الاسم', 'الحالة', 'المعدل', 'الترتيب']
                subjects = [c for c in df.columns if c not in exclude]
                
                pdf_data = create_pdf(student, subjects)
                st.download_button(label="📥 تحميل الشهادة PDF", data=pdf_data, file_name=f"result_{student['الاسم']}.pdf", mime="application/pdf")

                with st.expander("🔍 تفاصيل المواد"):
                    for s in subjects: st.write(f"**{s}:** {student[s]}")
            else:
                st.error("❌ الطالب غير موجود.")
    st.markdown('</div>', unsafe_allow_html=True)
