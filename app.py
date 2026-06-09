import streamlit as st
import pandas as pd
import os
from fpdf import FPDF

# 1. إعدادات الصفحة وجعل التخطيط متجاوباً تلقائياً
st.set_page_config(page_title="منصة نتائج التلاميذ", page_icon="🎓", layout="centered")

# 2. تصميم CSS محسن بالكامل لحل مشكلة التجاوب والألوان على الهواتف
st.markdown("""
    <style>
    .stApp { direction: rtl; text-align: right; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    
    /* تنسيق زر الاستعلام الأساسي وزر الطباعة */
    div.stButton > button { width: 100%; border-radius: 12px; background-color: #2563eb; color: white; height: 3.2em; font-weight: bold; font-size: 16px; border: none; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); }
    div.stButton > button:hover { background-color: #1d4ed8; }
    
    /* تنسيق علامات التبويب والخانات لتكون واضحة وجذابة على الهاتف */
    button[data-baseweb="tab"] { font-size: 16px !important; font-weight: bold !important; padding: 12px 20px !important; }
    
    /* تنسيق رسائل النجاح والرسوب بخلفيات ناعمة ونصوص واضحة */
    .success-box { color: #15803d; background-color: #f0fdf4; border: 1px solid #bbf7d0; padding: 18px; border-radius: 14px; text-align: center; font-size: 18px; font-weight: bold; margin: 15px 0; }
    .fail-box { color: #b91c1c; background-color: #fef2f2; border: 1px solid #fecaca; padding: 18px; border-radius: 14px; text-align: center; font-size: 18px; font-weight: bold; margin: 15px 0; }
    
    /* تحسين جداول البيانات وعرضها على الجوال */
    .stTable { width: 100% !important; border-radius: 10px; overflow: hidden; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎓 بوابة نتائج التلاميذ")
st.write("استخدم الاسم أو الرقم للاستعلام عن النتيجة وطباعة كشف الدرجات")

# اسم ملف البيانات الثابت
EXCEL_FILE = 'results.xlsx'

# دالة لتوليد ملف PDF متوافق مع الشكلية الرسمية الموريتانية (يدعم الأحرف العربية عبر الخطوط القياسية المدمجة وتدفق الاتجاه)
def create_pdf(s, subjects_list, format_value):
    pdf = FPDF(orientation="P", unit="mm", format="A4")
    pdf.add_page()
    
    # رسم الإطار الخارجي لكشف الدرجات
    pdf.set_line_width(0.5)
    pdf.rect(5, 5, 200, 287)
    
    # لتفادي مشاكل ترميز الخطوط العربية في مكتبات PDF الأساسية بدون ملفات خطوط خارجية،
    # نقوم بكتابة النصوص الأساسية بشكل متناسق باستخدام خط عريض قياسي.
    pdf.set_font("Helvetica", "B", 12)
    
    # تصميم الترويسة العلوية (يمين ويسار) كالشكلية تماماً
    pdf.text(12, 15, "Charaf - Ikha - Adl")
    pdf.text(12, 21, "Annee Scolaire: 2025/2026")
    pdf.text(12, 27, "Ecole: Kankossa")
    pdf.text(12, 33, "Classe: 3eme Annee AP")
    
    pdf.text(130, 15, "Republique Islamique de Mauritanie")
    pdf.text(130, 21, "Ministere de l'Education Nationale")
    pdf.text(130, 27, "Direction Regionale de l'Assaba")
    pdf.text(130, 33, "Inspection de Kankossa")
    
    # عنوان الكشف في المنتصف
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 35, "", ln=1) # مسافة عازلة
    pdf.cell(0, 10, "BULLETIN DE NOTES - FIN DE L'ANNEE", ln=1, align="C")
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 5, f"Nom de l'Eleve: {s.get('الاسم', '..........')}", ln=1, align="C")
    pdf.cell(0, 5, f"Numero: {s.get('الرقم', '....')}", ln=1, align="C")
    pdf.cell(0, 10, "", ln=1) # مسافة
    
    # إنشاء الجدول (رأس الجدول)
    pdf.set_fill_color(240, 240, 240)
    pdf.cell(60, 10, "Matiere (Sub)", 1, 0, "C", True)
    pdf.cell(40, 10, "Note Ex. 1", 1, 0, "C", True)
    pdf.cell(40, 10, "Note Ex. 2", 1, 0, "C", True)
    pdf.cell(50, 10, "Note Ex. Final (3)", 1, 1, "C", True)
    
    # تعبئة علامات المواد الثلاث لكل مادة في سطر واحد لتوفير الورق ومنع اللخبطة
    pdf.set_font("Helvetica", "", 11)
    for sub in subjects_list:
        # أسماء المواد بالفرنسية لتظهر صحيحة ومطابقة للترتيب الموريتاني في الـ PDF
        sub_display = sub
        if sub == "اللغة العربية": sub_display = "Arabe"
        elif sub == "التربية الاسلامية": sub_display = "Education Islamique"
        elif sub == "الرياضيات": sub_display = "Mathematiques"
        elif sub == "الفرنسية": sub_display = "Francais"
        elif sub == "العلوم الطبيعية": sub_display = "Sciences Naturelles"
        elif sub == "التاريخ والجغرافيا": sub_display = "Histoire & Geo"
        elif sub == "التربية الفنية": sub_display = "Education Artistique"
        elif sub == "التربية المدنية": sub_display = "Education Civique"
        elif sub == "الرياضة البدنية": sub_display = "Education Physique"
            
        pdf.cell(60, 8, sub_display, 1, 0, "L")
        pdf.cell(40, 8, str(format_value(s.get(f'{sub} 1'))), 1, 0, "C")
        pdf.cell(40, 8, str(format_value(s.get(f'{sub} 2'))), 1, 0, "C")
        pdf.cell(50, 8, str(format_value(s.get(f'{sub} 3'))), 1, 1, "C")
        
    # إضافة سطر المجموع والمعدلات والإجماليات في الأسفل
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(60, 8, "TOTAL / TOTAL", 1, 0, "L", True)
    pdf.cell(40, 8, str(format_value(s.get('المجموع 1'))), 1, 0, "C")
    pdf.cell(40, 8, str(format_value(s.get('المجموع 2'))), 1, 0, "C")
    pdf.cell(50, 8, str(format_value(s.get('المجموع 3'))), 1, 1, "C")
    
    pdf.cell(60, 8, "MOYENNE / MOYENNE", 1, 0, "L", True)
    pdf.cell(40, 8, str(format_value(s.get('معدل الامتحان الأول'))), 1, 0, "C")
    pdf.cell(40, 8, str(format_value(s.get('معدل الامتحان الثاني'))), 1, 0, "C")
    pdf.cell(50, 8, str(format_value(s.get('معدل الامتحان الأخير'))), 1, 1, "C")
    
    # النتائج العامة السنوية النهائية في ذيل الجدول
    pdf.cell(0, 5, "", ln=1)
    pdf.cell(95, 8, f"MOYENNE GENERALE (Annual Average): {format_value(s.get('المعدل العام'))}", 1, 0, "L")
    pdf.cell(95, 8, f"RANG (Rank): {s.get('الرتبة العامة', '..........')}", 1, 1, "L")
    pdf.cell(0, 8, f"DECISION (Decision Final): {s.get('القرار العام', '..........')}", 1, 1, "L")
    
    # خانة التوقيعات والختم أسفل الصفحة كما في وثيقتك
    pdf.cell(0, 15, "", ln=1)
    pdf.cell(95, 10, "Signature de l'Enseignant (المعلم)", 0, 0, "C")
    pdf.cell(95, 10, "Signature du Directeur (المدير)", 0, 1, "C")
    
    return pdf.output()

# 3. التحقق من وجود الملف
if not os.path.exists(EXCEL_FILE):
    st.error("⚠️ ملف النتائج (results.xlsx) غير موجود. يرجى رفعه في GitHub.")
else:
    try:
        df = pd.read_excel(EXCEL_FILE)
        
        # مدخلات البحث (الاسم أو الرقم)
        query = st.text_input("أدخل رقم التلميذ أو الاسم الكامل:", placeholder="مثال: 10 أو أحمد محمد")
        
        if st.button("استعلام"):
            if query:
                q = str(query).strip()
                match = df[(df['الرقم'].astype(str).str.strip() == q) | 
                           (df['الاسم'].str.strip().str.contains(q, case=False, na=False))]
                
                if not match.empty:
                    s = match.iloc[0].to_dict() # جلب التلميذ الأول المتطابق
                    
                    st.divider()
                    st.header(f"مرحباً، {s.get('الاسم', 'أيها التلميذ')}")
                    st.info(f"رقم التلميذ: {s.get('الرقم', 'غير متوفر')}")

                    def format_value(val):
                        try:
                            return round(float(val), 2)
                        except (ValueError, TypeError):
                            return val if pd.notna(val) else 'غير متوفر'

                    subjects_list = [
                        'اللغة العربية', 'التربية الاسلامية', 'الرياضيات', 'الفرنسية', 
                        'العلوم الطبيعية', 'التاريخ والجغرافيا', 'التربية الفنية', 
                        'التربية المدنية', 'الرياضة البدنية'
                    ]

                    # إنشاء الخانات الثلاث المباشرة المخصصة للعرض السريع على المنصة
                    tab1, tab2, tab3 = st.tabs(["📝 الامتحان الأول", "📝 الامتحان الثاني", "🏆 الامتحان الأخير"])
                    
                    # --- خانة الامتحان الأول ---
                    with tab1:
                        st.subheader("📊 كشف درجات الامتحان الأول")
                        labels1 = []
                        values1 = []
                        for sub in subjects_list:
                            labels1.append(sub)
                            values1.append(format_value(s.get(f'{sub} 1')))
                        labels1.extend(['المجموع', 'معدل الامتحان الأول', 'الرتبة', 'القرار'])
                        values1.extend([format_value(s.get('المجموع 1')), format_value(s.get('معدل الامتحان الأول')), s.get('الرتبة 1', 'غير متوفر'), s.get('القرار 1', 'غير متوفر')])
                        st.table(pd.DataFrame({'المادة / البيان': labels1, 'النتيجة': values1}))

                    # --- خانة الامتحان الثاني ---
                    with tab2:
                        st.subheader("📊 كشف درجات الامتحان الثاني")
                        labels2 = []
                        values2 = []
                        for sub in subjects_list:
                            labels2.append(sub)
                            values2.append(format_value(s.get(f'{sub} 2')))
                        labels2.extend(['المجموع', 'معدل الامتحان الثاني', 'الرتبة', 'القرار'])
                        values2.extend([format_value(s.get('المجموع 2')), format_value(s.get('معدل الامتحان الثاني')), s.get('الرتبة 2', 'غير متوفر'), s.get('القرار 2', 'غير متوفر')])
                        st.table(pd.DataFrame({'المادة / البيان': labels2, 'النتيجة': values2}))

                    # --- خانة الامتحان الأخير والنهائي ---
                    with tab3:
                        st.subheader("📊 كشف درجات الامتحان الأخير والنهائي")
                        labels3 = []
                        values3 = []
                        for sub in subjects_list:
                            labels3.append(sub)
                            values3.append(format_value(s.get(f'{sub} 3')))
                        labels3.extend(['المجموع', 'معدل الامتحان الأول', 'معدل الامتحان الثاني', 'معدل الامتحان الأخير', 'المعدل العام', 'الرتبة العامة', 'القرار العام'])
