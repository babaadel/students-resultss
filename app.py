import streamlit as st
import pandas as pd
from fpdf import FPDF
import os
from arabic_reshaper import reshape
from bidi.algorithm import get_display

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
    .fail-grade { color: #dc2626; font-weight: bold; }
    .pass-grade { color: #16a34a; font-weight: bold; }
    div.stButton > button { width: 100%; border-radius: 12px; background: linear-gradient(90deg, #2563eb, #1e40af); color: white; font-weight: bold; height: 3.5em; border: none; }
    </style>
    """, unsafe_allow_html=True)

# وظيفة لمعالجة النصوص العربية للـ PDF
def format_arabic(text):
    if pd.isna(text): return ""
    reshaped = reshape(str(text))
    return get_display(reshaped)

# 2. وظيفة إنشاء PDF المحدثة
def create_pdf(student_data, subjects):
    pdf = FPDF()
    pdf.add_page()
    
    # تأكد من وجود ملف الخط في المجلد (مثلاً Amiri-Regular.ttf)
    # يمكنك تحميله من Google Fonts
    try:
        pdf.add_font('Amiri', '', 'Amiri-Regular.ttf')
        pdf.set_font('Amiri', '', 16)
    except:
        # حل احتياطي إذا لم يجد الخط (سيظهر نص لاتيني فقط)
        pdf.set_font("Arial", size=12)

    pdf.cell(190, 10, txt=format_arabic("تقرير نتيجة الطالب"), ln=True, align='C')
    pdf.ln(10)
    
    pdf.set_font('Amiri', '', 12)
    pdf.cell(190, 10, txt=f"{format_arabic('الاسم')}: {format_arabic(student_data['الاسم'])}", ln=True, align='R')
    pdf.cell(190, 10, txt=f"{format_arabic('الرقم')}: {student_data['الرقم']}", ln=True, align='R')
    pdf.cell(190, 10, txt=f"{format_arabic('المعدل')}: {student_data.get('المعدل', 'N/A')}%", ln=True, align='R')
    
    pdf.ln(5)
    pdf.cell(190, 10, txt=format_arabic("تفاصيل المواد:"), ln=True, align='R')
    
    for subj in subjects:
        grade = student_data[subj]
        pdf.cell(190, 10, txt=f"{format_arabic(subj)}: {grade}", ln=True, align='R')
        
    return pdf.output()

# 3. تحميل البيانات
@st.cache_data
def load_data():
    file_path = "data.xlsx"
    if os.path.exists(file_path):
        try:
            df = pd.read_excel(file_path)
            if 'المعدل' in df.columns:
                df['الترتيب'] = df['المعدل'].rank(ascending=False, method='min').astype('Int64')
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
                    
                    rank_val = student.get("الترتيب", "N/A")
                    st_rank = f"{rank_val}#" if pd.notnull(rank_val) else "N/A"
                    c2.markdown(f'<div class="metric-card"><div class="metric-label">الترتيب</div><div class="metric-value">{st_rank}</div></div>', unsafe_allow_html=True)

                    exclude = ['الرقم', 'الاسم', 'الحالة', 'المعدل', 'الترتيب']
                    subjects = [c for c in df.columns if c not in exclude]
                    
                    # إنشاء الـ PDF
                    try:
                        pdf_bytes = create_pdf(student, subjects)
                        st.download_button("📥 تحميل الشهادة PDF", pdf_bytes, f"result_{student['الرقم']}.pdf", "application/pdf")
                    except Exception as e:
                        st.error(f"حدث خطأ أثناء إنشاء PDF: {e}")
                    
                    with st.expander("🔍 تفاصيل المواد (الأحمر يعني رسوب)"):
                        for s in subjects:
                            grade = student[s]
                            try:
                                if float(grade) < 50:
                                    st.markdown(f"**{s}:** <span class='fail-grade'>{grade}</span>", unsafe_allow_html=True)
                                else:
                                    st.markdown(f"**{s}:** <span class='pass-grade'>{grade}</span>", unsafe_allow_html=True)
                            except:
                                st.write(f"**{s}:** {grade}")
                else:
                    st.error("❌ لم يتم العثور على الطالب.")
        st.markdown('</div>', unsafe_allow_html=True)
else:
    st.error("⚠️ يرجى التأكد من رفع ملف data.xlsx بجانب هذا الكود.")
