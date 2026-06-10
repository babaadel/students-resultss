import streamlit as st
import pandas as pd
import os

# 1. إعدادات الصفحة وجعل التخطيط متجاوباً تلقائياً
st.set_page_config(page_title="منصة نتائج التلاميذ", page_icon="🎓", layout="centered")

# 2. تصميم CSS محسن بالكامل لحل مشكلة التجاوب والألوان على الهواتف
st.markdown("""
    <style>
    .stApp { direction: rtl; text-align: right; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    
    /* تنسيق زر الاستعلام الأساسي */
    div.stButton > button { width: 100%; border-radius: 12px; background-color: #2563eb; color: white; height: 3.2em; font-weight: bold; font-size: 16px; border: none; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); }
    div.stButton > button:hover { background-color: #1d4ed8; }
    
    /* تنسيق علامات التبويب والخانات لتكون واضحة وجذابة على الهاتف */
    button[data-baseweb="tab"] { font-size: 16px !important; font-weight: bold !important; padding: 12px 20px !important; }
    
    /* تنسيق رسائل النجاح والرسوب بخلفيات ناعمة ونصوص واضحة */
    .success-box { color: #15803d; background-color: #f0fdf4; border: 1px solid #bbf7d0; padding: 18px; border-radius: 14px; text-align: center; font-size: 18px; font-weight: bold; margin: 15px 0; }
    .fail-box { color: #b91c1c; background-color: #fef2f2; border: 1px solid #fecaca; padding: 18px; border-radius: 14px; text-align: center; font-size: 18px; font-weight: bold; margin: 15px 0; }
    
    /* تحسين جداول البيانات وعرضها على الجوال */
    .stTable { width: 100% !important; border-radius: 10px; overflow: hidden; }

    /* ===== زر الطباعة ===== */
    .print-btn {
        display: block; width: 100%; padding: 12px;
        background-color: #16a34a; color: white;
        border: none; border-radius: 10px;
        font-size: 16px; font-weight: bold;
        cursor: pointer; margin: 12px 0;
        font-family: 'Segoe UI', Tahoma, sans-serif;
    }
    .print-btn:hover { background-color: #15803d; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎓 بوابة نتائج التلاميذ")
st.write("استخدم الاسم أو الرقم للاستعلام عن النتيجة")

# ===== دالة توليد HTML شكلية الكشف الرسمي =====
def build_report_html(s, subjects_list, format_value, exam_num):
    """توليد HTML كامل لشكلية الكشف الرسمي الموريتاني"""

    if exam_num == 1:
        exam_title = "امتحان الفصل الأول"
        avg_key = 'معدل الامتحان الأول'
        rank_key = 'الرتبة 1'
        decision_key = 'القرار 1'
        suffix = '1'
    elif exam_num == 2:
        exam_title = "امتحان الفصل الثاني"
        avg_key = 'معدل الامتحان الثاني'
        rank_key = 'الرتبة 2'
        decision_key = 'القرار 2'
        suffix = '2'
    else:
        exam_title = "امتحان الفصل الأخير"
        avg_key = 'معدل الامتحان الأخير'
        rank_key = 'الرتبة العامة'
        decision_key = 'القرار العام'
        suffix = '3'

    avg1 = format_value(s.get('معدل الامتحان الأول'))
    avg2 = format_value(s.get('معدل الامتحان الثاني'))
    avg3 = format_value(s.get('معدل الامتحان الأخير'))
    avg_general = format_value(s.get('المعدل العام'))
    rank_val = s.get(rank_key, '')
    decision_val = str(s.get(decision_key, ''))
    total_val = format_value(s.get(f'المجموع {suffix}'))
    exam_avg = format_value(s.get(avg_key))

    # لون القرار
    if "ناجح" in decision_val or "منتقل" in decision_val:
        dec_color = "#16a34a"
    else:
        dec_color = "#dc2626"

    # صفوف المواد
    rows_html = ""
    for sub in subjects_list:
        val = format_value(s.get(f'{sub} {suffix}'))
        rows_html += f"""
        <tr>
            <td style="border:1px solid #333;padding:6px 10px;text-align:right;">{sub}</td>
            <td style="border:1px solid #333;padding:6px 10px;text-align:center;">{val}</td>
            <td rowspan="0" style="display:none;"></td>
        </tr>"""

    html = f"""<!DOCTYPE html>
<html dir="rtl" lang="ar">
<head>
<meta charset="UTF-8">
<title>كشف درجات - {s.get('الاسم','')}</title>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: 'Traditional Arabic', 'Amiri', 'Segoe UI', Tahoma, sans-serif; direction: rtl; background: white; color: #111; padding: 20px; }}
  .outer-border {{ border: 3px solid #000; padding: 10px; max-width: 780px; margin: auto; }}
  .top-header {{ display: flex; justify-content: space-between; align-items: flex-start; border-bottom: 2px solid #000; padding-bottom: 10px; margin-bottom: 10px; }}
  .top-header .col {{ font-size: 13px; line-height: 1.9; }}
  .top-header .col-center {{ text-align: center; }}
  .top-header .col-center img {{ width: 90px; height: 90px; object-fit: contain; }}
  .top-header strong {{ font-size: 14px; }}
  .motto {{ font-size: 12px; color: #555; text-align: left; margin-bottom: 4px; }}
  .exam-title {{ text-align: center; font-size: 22px; font-weight: bold; margin: 10px 0 4px 0; border-bottom: 1px solid #ccc; padding-bottom: 6px; }}
  .kashf-title {{ text-align: center; background: #d4edda; border: 1px solid #aaa; border-radius: 6px; font-size: 20px; font-weight: bold; padding: 6px 20px; margin: 8px auto; width: fit-content; }}
  .student-info {{ display: flex; justify-content: space-between; font-size: 13px; margin: 10px 0; padding: 0 4px; }}
  .student-info span {{ font-weight: bold; color: #1a56db; }}
  table {{ width: 100%; border-collapse: collapse; margin-top: 6px; font-size: 13px; }}
  th {{ background: #f0f0f0; border: 1px solid #333; padding: 7px 10px; text-align: center; font-size: 13px; }}
  td {{ border: 1px solid #333; padding: 6px 10px; }}
  .avg-cell {{ text-align: center; font-weight: bold; color: #c00; font-size: 15px; }}
  .decision-cell {{ text-align: center; font-weight: bold; font-size: 20px; color: {dec_color}; }}
  .footer-row {{ display: flex; justify-content: space-between; margin-top: 20px; font-size: 14px; font-weight: bold; border-top: 1px solid #aaa; padding-top: 10px; }}
  @media print {{
    body {{ padding: 8px; }}
    .no-print {{ display: none; }}
  }}
</style>
</head>
<body>
<div class="outer-border">

  <!-- الترويسة الرسمية -->
  <div class="top-header">
    <div class="col" style="text-align:right;">
      <strong>الجمهورية الإسلامية الموريتانية</strong><br>
      وزارة التربية وإصلاح النظام التعليمي<br>
      الإدارة الجهوية بولاية لعصابه<br>
      مفتشية التعليم بمقاطعة كنكوصة
    </div>
    <div class="col col-center">
      <!-- شعار موريتانيا نصي بديل -->
      <div style="font-size:48px;">🇲🇷</div>
      <div style="font-size:10px;color:#555;">REPUBLIQUE ISLAMIQUE DE MAURITANIE</div>
    </div>
    <div class="col" style="text-align:left;">
      <div class="motto">شـرف – إخـاء – عـدل</div>
      <strong>العام الدراسي: 2025\2026</strong><br>
      المـــدرسة: كنكوصة 4<br>
      القسـم: الثالث ابتدائي
    </div>
  </div>

  <!-- عنوان الامتحان والكشف -->
  <div class="exam-title">{exam_title}</div>
  <div class="kashf-title">كشف الدرجات</div>

  <!-- معلومات التلميذ -->
  <div class="student-info">
    <div>الاسم الكامل: <span>{s.get('الاسم','')}</span></div>
    <div>الرقم المدرسي: <span>{s.get('الرقم','')}</span></div>
    <div>رقم النداء: <span>{s.get('الرقم','')}</span></div>
  </div>

  <!-- جدول الدرجات الرئيسي -->
  <table>
    <thead>
      <tr>
        <th>المواد</th>
        <th>الدرجات</th>
        <th>معدل الامتحان الاول</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td style="text-align:right;">اللغة العربية</td>
        <td style="text-align:center;">{format_value(s.get(f'اللغة العربية {suffix}'))}</td>
        <td rowspan="3" class="avg-cell">{avg1}\20</td>
      </tr>
      <tr>
        <td style="text-align:right;">التربية الإسلامية</td>
        <td style="text-align:center;">{format_value(s.get(f'التربية الاسلامية {suffix}'))}</td>
      </tr>
      <tr>
        <td style="text-align:right;">الرياضيات</td>
        <td style="text-align:center;">{format_value(s.get(f'الرياضيات {suffix}'))}</td>
      </tr>
      <tr>
        <td style="text-align:right;">الفرنسية</td>
        <td style="text-align:center;">{format_value(s.get(f'الفرنسية {suffix}'))}</td>
        <th style="text-align:center;background:#f0f0f0;">الملاحظات</th>
      </tr>
      <tr>
        <td style="text-align:right;">العلوم الطبيعية</td>
        <td style="text-align:center;">{format_value(s.get(f'العلوم الطبيعية {suffix}'))}</td>
        <td rowspan="3" class="avg-cell">{avg2}\20</td>
      </tr>
      <tr>
        <td style="text-align:right;">التاريخ والجغرافيا</td>
        <td style="text-align:center;">{format_value(s.get(f'التاريخ والجغرافيا {suffix}'))}</td>
      </tr>
      <tr>
        <td style="text-align:right;">التربية المدنية</td>
        <td style="text-align:center;">{format_value(s.get(f'التربية المدنية {suffix}'))}</td>
      </tr>
      <tr>
        <td style="text-align:right;">التربية الفنية</td>
        <td style="text-align:center;">{format_value(s.get(f'التربية الفنية {suffix}'))}</td>
        <th style="text-align:center;background:#f0f0f0;">معدل الامتحان الثالث</th>
      </tr>
      <tr>
        <td style="text-align:right;">الرياضة البدنية</td>
        <td style="text-align:center;">{format_value(s.get(f'الرياضة البدنية {suffix}'))}</td>
        <td rowspan="4" class="avg-cell">{avg3}\20</td>
      </tr>
      <tr>
        <td style="text-align:right;">المجموع</td>
        <td style="text-align:center;">{total_val}\200</td>
      </tr>
      <tr>
        <td style="text-align:right;font-weight:bold;">المعدل</td>
        <td style="text-align:center;font-weight:bold;color:#c00;">{exam_avg}\20</td>
      </tr>
      <tr>
        <td colspan="2" style="text-align:center;">
          المعدل العام: <strong style="color:#16a34a;">{avg_general}</strong>
        </td>
      </tr>
      <tr>
        <td colspan="2" style="text-align:center;font-size:13px;">
          الرتبة: <strong>{rank_val}</strong>
        </td>
        <td class="decision-cell">{decision_val}</td>
      </tr>
    </tbody>
  </table>

  <!-- توقيعات -->
  <div class="footer-row">
    <div>المعلم: ________________</div>
    <div>المدير: ________________</div>
  </div>

</div>

<script>
  window.onload = function() {{ window.print(); }}
</script>
</body>
</html>"""
    return html


# ===== JavaScript لفتح نافذة الطباعة =====
st.markdown("""
<script>
function openPrintWindow(htmlContent) {
    const win = window.open('', '_blank', 'width=850,height=1100');
    win.document.write(htmlContent);
    win.document.close();
}
</script>
""", unsafe_allow_html=True)

# اسم ملف البيانات الثابت
EXCEL_FILE = 'results.xlsx'

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
                # تنظيف النص وتغيير نوع البيانات للبحث المرن
                q = str(query).strip()
                match = df[(df['الرقم'].astype(str).str.strip() == q) | 
                           (df['الاسم'].str.strip().str.contains(q, case=False, na=False))]
                
                if not match.empty:
                    s = match.iloc[0].to_dict() # جلب التلميذ الأول المتطابق
                    
                    st.divider()
                    st.header(f"مرحباً، {s.get('الاسم', 'أيها التلميذ')}")
                    st.info(f"رقم التلميذ: {s.get('الرقم', 'غير متوفر')}")

                    # دالة مساعدة لتقريب المعدلات والدرجات لرقمين فقط بعد الفاصلة
                    def format_value(val):
                        try:
                            return round(float(val), 2)
                        except (ValueError, TypeError):
                            return val if pd.notna(val) else 'غير متوفر'

                    # قائمة المواد الثابتة المطلوبة بكل امتحان
                    subjects_list = [
                        'اللغة العربية', 'التربية الاسلامية', 'الرياضيات', 'الفرنسية', 
                        'العلوم الطبيعية', 'التاريخ والجغرافيا', 'التربية الفنية', 
                        'التربية المدنية', 'الرياضة البدنية'
                    ]

                    # إنشاء الخانات الثلاث المباشرة (الامتحانات)
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
                        values1.extend([
                            format_value(s.get('المجموع 1')),
                            format_value(s.get('معدل الامتحان الأول')),
                            s.get('الرتبة 1', 'غير متوفر'),
                            s.get('القرار 1', 'غير متوفر')
                        ])
                            
                        st.table(pd.DataFrame({'المادة / البيان': labels1, 'النتيجة': values1}))

                        # ===== زر طباعة الشكلية الرسمية =====
                        report1_html = build_report_html(s, subjects_list, format_value, exam_num=1)
                        report1_escaped = report1_html.replace('`', '\\`').replace('${', '\\${')
                        st.markdown(f"""
                        <button class="print-btn" onclick="openPrintWindow(`{report1_escaped}`)">
                            🖨️ طباعة الشكلية الرسمية — الامتحان الأول
                        </button>
                        """, unsafe_allow_html=True)

                    # --- خانة الامتحان الثاني ---
                    with tab2:
                        st.subheader("📊 كشف درجات الامتحان الثاني")
                        labels2 = []
                        values2 = []
                        
                        for sub in subjects_list:
                            labels2.append(sub)
                            values2.append(format_value(s.get(f'{sub} 2')))
                        
                        labels2.extend(['المجموع', 'معدل الامتحان الثاني', 'الرتبة', 'القرار'])
                        values2.extend([
                            format_value(s.get('المجموع 2')),
                            format_value(s.get('معدل الامتحان الثاني')),
                            s.get('الرتبة 2', 'غير متوفر'),
                            s.get('القرار 2', 'غير متوفر')
                        ])
                            
                        st.table(pd.DataFrame({'المادة / البيان': labels2, 'النتيجة': values2}))

                        # ===== زر طباعة الشكلية الرسمية =====
                        report2_html = build_report_html(s, subjects_list, format_value, exam_num=2)
                        report2_escaped = report2_html.replace('`', '\\`').replace('${', '\\${')
                        st.markdown(f"""
                        <button class="print-btn" onclick="openPrintWindow(`{report2_escaped}`)">
                            🖨️ طباعة الشكلية الرسمية — الامتحان الثاني
                        </button>
                        """, unsafe_allow_html=True)

                    # --- خانة الامتحان الأخير والنهائي ---
                    with tab3:
                        st.subheader("📊 كشف درجات الامتحان الأخير والنهائي")
                        labels3 = []
                        values3 = []
                        
                        for sub in subjects_list:
                            labels3.append(sub)
                            values3.append(format_value(s.get(f'{sub} 3')))
                        
                        labels3.extend([
                            'المجموع', 
                            'معدل الامتحان الأول', 
                            'معدل الامتحان الثاني', 
                            'معدل الامتحان الأخير', 
                            'المعدل العام', 
                            'الرتبة العامة', 
                            'القرار العام'
                        ])
                        values3.extend([
                            format_value(s.get('المجموع 3')),
                            format_value(s.get('معدل الامتحان الأول')),
                            format_value(s.get('معدل الامتحان الثاني')),
                            format_value(s.get('معدل الامتحان الأخير')),
                            format_value(s.get('المعدل العام')),
                            s.get('الرتبة العامة', 'غير متوفر'),
                            s.get('القرار العام', 'غير متوفر')
                        ])
                            
                        st.table(pd.DataFrame({'المادة / البيان': labels3, 'النتيجة': values3}))
                        
                        # ===== زر طباعة الشكلية الرسمية =====
                        report3_html = build_report_html(s, subjects_list, format_value, exam_num=3)
                        report3_escaped = report3_html.replace('`', '\\`').replace('${', '\\${')
                        st.markdown(f"""
                        <button class="print-btn" onclick="openPrintWindow(`{report3_escaped}`)">
                            🖨️ طباعة الشكلية الرسمية — الامتحان الأخير
                        </button>
                        """, unsafe_allow_html=True)

                        # عرض رسالة النجاح الكبرى بناءً على النتيجة النهائية للعام الدراسي (القرار العام)
                        dec_general = str(s.get('القرار العام', ''))
                        if "ناجح" in dec_general or "منتقل" in dec_general:
                            st.markdown(f'<div class="success-box">🏆 النتيجة النهائية للعام الدراسي: {dec_general} 🎈</div>', unsafe_allow_html=True)
                            st.balloons()
                        elif "راسب" in dec_general or "مكرر" in dec_general:
                            st.markdown(f'<div class="fail-box">😔 النتيجة النهائية للعام الدراسي: {dec_general} 💔</div>', unsafe_allow_html=True)
                                
                else:
                    st.error(f"❌ لم يتم العثور على نتيجة لـ '{query}'.")
            else:
                st.info("يرجى كتابة الاسم أو الرقم أولاً.")
    except Exception as e:
        st.error(f"حدث خطأ في قراءة البيانات: {e}")
