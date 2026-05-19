import streamlit as st
import pandas as pd
from fpdf import FPDF

# --- 1. إعدادات الصفحة والتصميم ---
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
    .stTextInput > div > div > input { text-align: center; border-radius: 12px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. وظيفة إنشاء ملف PDF ---
def create_pdf(student_data, subjects):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="Student Result Report", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Student Name: {student_data['الاسم']}", ln=True)
    pdf.cell(200, 10, txt=f"Student ID: {student_data['الرقم']}", ln=True)
    pdf.cell(200, 10, txt=f"GPA: {student_data.get('المعدل', 'N/A')}%", ln=True)
    pdf.cell(200, 10, txt=f"Rank: {student_data.get('الترتيب', 'N/A')}", ln=True)
    pdf.ln(10)
    pdf.cell(200, 10, txt="Grades Details:", ln=True)
    for subj in subjects:
        pdf.cell(200, 10, txt=f"- {subj}: {student_data[subj]}", ln=True)
    return bytes(pdf.output())

# --- 3. تحميل البيانات ---
@st.cache_data
def load_data():
    try:
        df = pd.read_excel("data.xlsx")
        # حساب الترتيب تلقائياً إذا وجد المعدل
        if 'المعدل' in df.columns and 'الترتيب' not in df.columns:
            df['الترتيب'] = df['المعدل'].rank(ascending=False, method='min').astype(int)
        return df
    except:
        return None

df = load_data()

# --- 4. واجهة المستخدم ---
st.markdown("<h1 style='text-align: center; color: #1e40af;'>🎓 منصة استعلام النتائج</h1>", unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="stCard">', unsafe_allow_html=True)
    
    search_query = st.text_input("أدخل اسم الطالب أو رقمه التسلسلي:", placeholder="مثال: أحمد أو 12345")
    search_btn = st.button("استعلام عن النتيجة")
    
    if search_btn and search_query:
        if df is not None:
            query_str = str(search_query).strip()
            # البحث بالاسم أو الرقم
            result = df[(df['الرقم'].astype(str) == query_str) | (df['الاسم'].str.contains(query_str, na=False))]
            
            if not result.empty:
                student = result.iloc[0]
                status = str(student.get('الحالة', 'ناجح'))

                # منطق البالونات والإيموجي
                if "ناجح" in status:
                    st.balloons()
                    st.success(f"🎉 مبارك النجاح! الطالب: {student['الاسم']}")
                else:
                    st.markdown("<h1 style='text-align: center;'>😔</h1>", unsafe_allow_html=True)
                    st.error(f"نتمنى لك التوفيق في المرة القادمة. الطالب: {student['الاسم']}")

                # عرض المعدل والترتيب
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f'<div class="metric-card"><div class="metric-label">المعدل العام</div><div class="metric-value">{student.get("المعدل", "N/A")}%</div></div>', unsafe_allow_html=True)
                with col2:
                    st.markdown(f'<div class="metric-card"><div class="metric-label">الترتيب</div><div class="metric-value">{student.get("الترتيب", "N/A")}#</div></div>', unsafe_allow_html=True)

                st.write("---")

                # إعداد بيانات المواد والـ PDF
                exclude = ['الرقم', 'الاسم', 'الحالة', 'المعدل', 'الترتيب']
                subjects = [c for c in df.columns if c not in exclude]
                
                # زر تحميل الـ PDF
                try:
                    pdf_bytes = create_pdf(student, subjects)
                    st.download_button(label="📥 تحميل الشهادة PDF", data=pdf_bytes, file_name=f"result_{student['الرقم']}.pdf", mime="application/pdf")
                except:
                    st.warning("حدث خطأ أثناء تجهيز ملف PDF.")

                # تفاصيل المواد في قائمة منسدلة
                with st.expander("🔍 عرض تفاصيل درجات المواد"):
                    for s in subjects:
                        st.write(f"**{s}:** {student[s]}")
            else:
                st.error("❌ لم يتم العثور على طالب بهذا الاسم أو الرقم.")
        else:
            st.error("⚠️ فشل تحميل ملف البيانات data.xlsx. تأكد من وجوده بجانب الكود.")
    
    st.markdown('</div>', unsafe_allow_html=True)
