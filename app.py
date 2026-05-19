import streamlit as st
import pandas as pd
from fpdf import FPDF
import os

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة التميز للنتائج", page_icon="🎓", layout="centered")

st.markdown("""
    <style>
    @import url('https://googleapis.com');
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif; text-align: right; direction: rtl; }
    .main { background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); }
    .stCard { background: white; padding: 25px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); border-top: 5px solid #2563eb; margin-bottom: 20px; }
    .metric-card { background: #f8fafc; padding: 15px; border-radius: 10px; text-align: center; border: 1px solid #e2e8f0; }
    .metric-value { font-size: 22px; font-weight: bold; color: #2563eb; }
    .metric-label { font-size: 14px; color: #64748b; }
    div.stButton > button { width: 100%; border-radius: 12px; background: linear-gradient(90deg, #2563eb, #1e40af); color: white; font-weight: bold; height: 3.5em; border: none; }
    </style>
    """, unsafe_allow_html=True)

# 2. وظيفة إنشاء PDF
def create_pdf(student_data, subjects):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="Student Result Report", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"ID: {student_data['الرقم']}", ln=True)
    pdf.cell(200, 10, txt=f"GPA: {student_data.get('المعدل', 'N/A')}%", ln=True)
    for subj in subjects:
        pdf.cell(200, 10, txt=f"- {subj}: {student_data[subj]}", ln=True)
    return bytes(pdf.output())

# 3. تحميل البيانات مع التحقق من وجود الملف
@st.cache_data
def load_data():
    file_path = "data.xlsx"
    if os.path.exists(file_path):
        try:
            df = pd.read_excel(file_path)
            if 'المعدل' in df.columns and 'الترتيب' not in df.columns:
                df['الترتيب'] = df['المعدل'].rank(ascending=False, method='min').astype(int)
            return df
        except Exception as e:
            st.error(f"خطأ في قراءة الملف: {e}")
            return None
    return None

df = load_data()

# 4. الواجهة
st.markdown("<h1 style='text-align: center; color: #1e40af;'>🎓 منصة استعلام النتائج</h1>", unsafe_allow_html=True)

if df is not None:
    with st.container():
        st.markdown('<div class="stCard">', unsafe_allow_html=True)
        search_query = st.text_input("أدخل الاسم أو الرقم:", placeholder="اكتب هنا...")
        if st.button("استعلام"):
            if search_query:
                query_str = str(search_query).strip()
                result = df[(df['الرقم'].astype(str) == query_str) | (df['الاسم'].str.contains(query_str, na=False))]
                
                if not result.empty:
                    student = result.iloc[0]
                    status = str(student.get('الحالة', 'ناجح'))
                    
                    if "ناجح" in status:
                        st.success(f"🎉 مبارك النجاح! {student['الاسم']}")
                        st.balloons()
                    else:
                        st.markdown("<h1 style='text-align: center;'>😔</h1>", unsafe_allow_html=True)
                        st.error(f"حظ أوفر.. {student['الاسم']}")

                    c1, c2 = st.columns(2)
                    c1.markdown(f'<div class="metric-card"><div class="metric-label">المعدل</div><div class="metric-value">{student.get("المعدل", "N/A")}%</div></div>', unsafe_allow_html=True)
                    c2.markdown(f'<div class="metric-card"><div class="metric-label">الترتيب</div><div class="metric-value">{student.get("الترتيب", "N/A")}#</div></div>', unsafe_allow_html=True)

                    exclude = ['الرقم', 'الاسم', 'الحالة', 'المعدل', 'الترتيب']
                    subjects = [c for c in df.columns if c not in exclude]
                    
                    pdf_bytes = create_pdf(student, subjects)
                    st.download_button("📥 تحميل الشهادة PDF", pdf_bytes, f"result_{student['الرقم']}.pdf", "application/pdf")
                    
                    with st.expander("🔍 تفاصيل المواد"):
                        for s in subjects: st.write(f"**{s}:** {student[s]}")
                else:
                    st.error("❌ لم يتم العثور على الطالب.")
        st.markdown('</div>', unsafe_allow_html=True)
else:
    st.error("⚠️ يرجى التأكد من رفع ملف data.xlsx بجانب هذا الكود على GitHub.")
