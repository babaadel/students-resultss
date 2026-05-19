import streamlit as st
import pandas as pd
from fpdf2 import FPDF

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة التميز للنتائج", page_icon="🎓", layout="centered")

# تنسيق CSS
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

# 2. وظيفة إنشاء ملف PDF (مبسطة لتجنب مشاكل الترميز)
def create_pdf(student_data, subjects):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="Student Result Report", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Student ID: {student_data['الرقم']}", ln=True)
    pdf.cell(200, 10, txt=f"GPA: {student_data.get('المعدل', 'N/A')}%", ln=True)
    pdf.ln(5)
    for subj in subjects:
        pdf.cell(200, 10, txt=f"- {subj}: {student_data[subj]}", ln=True)
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
    
    # حقل الإدخال
    search_query = st.text_input("أدخل الاسم أو الرقم التسلسلي:", placeholder="مثال: محمد أو 1001")
    
    # إعادة زر البحث (Search Button)
    search_btn = st.button("استعلام الآن")
    
    if search_btn:
        if search_query:
            if df is not None:
                query_str = str(search_query).strip()
                result = df[(df['الرقم'].astype(str) == query_str) | (df['الاسم'].str.contains(query_str, na=False))]
                
                if not result.empty:
                    student = result.iloc[0]
                    status = str(student.get('الحالة', 'ناجح'))

                    if "ناجح" in status:
                        st.balloons()
                        st.success(f"🎉 مبارك النجاح! الطالب: {student['الاسم']}")
                    else:
                        st.markdown("<h1 style='text-align: center;'>😔</h1>", unsafe_allow_html=True)
                        st.error(f"حظ أوفر.. الطالب: {student['الاسم']}")

                    # عرض المعدل والترتيب
                    c1, c2 = st.columns(2)
                    with c1:
                        st.markdown(f'<div class="metric-card"><div class="metric-label">المعدل</div><div class="metric-value">{student.get("المعدل", "N/A")}%</div></div>', unsafe_allow_html=True)
                    with c2:
                        st.markdown(f'<div class="metric-card"><div class="metric-label">الترتيب</div><div class="metric-value">{student.get("الترتيب", "N/A")}#</div></div>', unsafe_allow_html=True)

                    st.markdown("<br>", unsafe_allow_html=True)

                    # زر PDF والتفاصيل
                    exclude = ['الرقم', 'الاسم', 'الحالة', 'المعدل', 'الترتيب']
                    subjects = [c for c in df.columns if c not in exclude]
                    
                    try:
                        pdf_data = create_pdf(student, subjects)
                        st.download_button(label="📥 تحميل الشهادة PDF", data=pdf_data, file_name=f"result_{student['الرقم']}.pdf", mime="application/pdf")
                    except:
                        st.warning("تعذر إنشاء ملف PDF حالياً.")

                    with st.expander("🔍 عرض درجات المواد التفصيلية"):
                        for s in subjects:
                            st.write(f"**{s}:** {student[s]}")
                else:
                    st.error("❌ لم يتم العثور على طالب بهذا الاسم أو الرقم.")
            else:
                st.error("⚠️ ملف البيانات data.xlsx غير موجود!")
        else:
            st.warning("⚠️ يرجى كتابة شيء في مربع البحث أولاً.")
            
    st.markdown('</div>', unsafe_allow_html=True)
