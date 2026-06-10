import streamlit as st
import pandas as pd
import os

# 1. إعدادات الصفحة وجعل التخطيط متجاوباً تلقائياً
st.set_page_config(page_title="منصة نتائج التلاميذ", page_icon="🎓", layout="centered")

# 2. تصميم CSS محسن بالكامل لواجهة الموقع
st.markdown("""
    <style>
    .stApp { direction: rtl; text-align: right; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    
    /* تنسيق زر الاستعلام الأساسي */
    div.stButton > button { width: 100%; border-radius: 12px; background-color: #2563eb; color: white; height: 3.2em; font-weight: bold; font-size: 16px; border: none; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); }
    div.stButton > button:hover { background-color: #1d4ed8; }
    
    /* تنسيق علامات التبويب والخانات */
    button[data-baseweb="tab"] { font-size: 16px !important; font-weight: bold !important; padding: 12px 20px !important; }
    
    /* تنسيق رسائل النجاح والرسوب في الواجهة */
    .success-box { color: #15803d; background-color: #f0fdf4; border: 1px solid #bbf7d0; padding: 18px; border-radius: 14px; text-align: center; font-size: 18px; font-weight: bold; margin: 15px 0; }
    .fail-box { color: #b91c1c; background-color: #fef2f2; border: 1px solid #fecaca; padding: 18px; border-radius: 14px; text-align: center; font-size: 18px; font-weight: bold; margin: 15px 0; }
    
    /* تحسين جداول البيانات */
    .stTable { width: 100% !important; border-radius: 10px; overflow: hidden; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎓 بوابة نتائج التلاميذ")
st.write("استخدم الاسم أو الرقم للاستعلام عن النتيجة")

# ===== دالة توليد HTML لشكلية الكشف الرسمي الموريتاني المحسن =====
def build_report_html(s, format_value, exam_num):
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
    rank_val = s.get(rank_key, 'غير متوفر')
    decision_val = str(s.get(decision_key, 'غير متوفر'))
    total_val = format_value(s.get(f'المجموع {suffix}'))
    exam_avg = format_value(s.get(avg_key))

    if "ناجح" in decision_val or "منتقل" in decision_val:
        dec_color = "#16a34a"
    else:
        dec_color = "#dc2626"

    # رابط الشعار الموريتاني الرسمي الدائري الملون
    logo_url = "https://upload.wikimedia.org/wikipedia/commons/4/43/Seal_of_Mauritania.svg"

    html_template = """<!DOCTYPE html>
<html dir="rtl" lang="ar">
<head>
<meta charset="UTF-8">
<title>كشف درجات</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { font-family: 'Segoe UI', Tahoma, sans-serif; direction: rtl; background: white; color: #111; padding: 20px; }
  .outer-border { border: 3px solid #000; padding: 10px; max-width: 780px; margin: auto; }
  
  /* ترويسة خلفية العلم الموريتاني المتدرج */
  .top-header { 
    display: flex; 
    justify-content: space-between; 
    align-items: center; 
    background: linear-gradient(135deg, #d2143a 0%, #00a95c 15%, #00a95c 85%, #d2143a 100%);
    padding: 15px; 
    border-radius: 8px;
    border: 2px solid #ffca28;
    color: white;
    margin-bottom: 15px; 
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
  }
  .top-header .col { font-size: 13px; line-height: 1.8; font-weight: 500; }
  .top-header .col-center { text-align: center; }
  .top-header .col-center img { width: 90px; height: 90px; filter: drop-shadow(0px 2px 4px rgba(0,0,0,0.3)); }
  .top-header strong { font-size: 14px; color: #ffca28; }
  .motto { font-size: 12px; color: #eaeaea; text-align: left; margin-bottom: 4px; font-weight: bold; }
  
  /* تنسيق موحد للعناوين وبنفس الحجم */
  .titles-container { display: flex; flex-direction: column; align-items: center; gap: 8px; margin: 15px 0; }
  .exam-title { text-align: center; font-size: 20px; font-weight: bold; color: #111; background: #f8f9fa; padding: 6px 25px; border-radius: 6px; border: 1px solid #ccc; width: fit-content; }
  .kashf-title { text-align: center; font-size: 20px; font-weight: bold; color: #15803d; background: #e8f5e9; padding: 6px 25px; border-radius: 6px; border: 1px solid #a5d6a7; width: fit-content; }
  
  .student-info { display: flex; justify-content: space-between; font-size: 13px; margin: 15px 0; padding: 8px; background: #f8f9fa; border-radius: 6px; border: 1px solid #eee; }
  .student-info span { font-weight: bold; color: #2563eb; }
  
  table { width: 100%; border-collapse: collapse; margin-top: 10px; font-size: 13px; }
  th { background: #f1f5f9; border: 1px solid #334155; padding: 8px 10px; text-align: center; color: #1e293b; font-weight: bold; }
  td { border: 1px solid #334155; padding: 7px 10px; }
  .avg-cell { text-align: center; font-weight: bold; color: #b91c1c; font-size: 14px; background: #fffaf0; }
  .decision-cell { text-align: center; font-weight: bold; font-size: 22px; color: __DEC_COLOR__; }
  .footer-row { display: flex; justify-content: space-between; margin-top: 25px; font-size: 14px; font-weight: bold; border-top: 2px dashed #ccc; padding-top: 15px; }
</style>
</head>
<body>
<div class="outer-border">
  
  <div class="top-header">
    <div class="col" style="text-align:right;">
      <strong>الجمهورية الإسلامية الموريتانية</strong><br>
      وزارة التربية وإصلاح النظام التعليمي<br>
      الإدارة الجهوية بولاية لعصابه<br>
      مفتشية التعليم بمقاطعة كنكوصة
    </div>
    <div class="col col-center">
      <img src="__LOGO_URL__" alt="الشعار الرسمي">
    </div>
    <div class="col" style="text-align:left;">
      <div class="motto">شـرف – إخـاء – عـدل</div>
      <strong>العام الدراسي: 2025\\2026</strong><br>
      المـــدرسة: كنكوصة 4<br>
      القسـم: الثالث ابتدائي
    </div>
  </div>

  <div class="titles-container">
    <div class="exam-title">__EXAM_TITLE__</div>
    <div class="kashf-title">كشف الدرجات</div>
  </div>

  <div class="student-info">
    <div>الاسم الكامل: <span>__STUDENT_NAME__</span></div>
    <div>الرقم المدرسي: <span>__STUDENT_ID__</span></div>
    <div>رقم النداء: <span>__STUDENT_ID__</span></div>
  </div>

  <table>
    <thead>
      <tr>
        <th>المواد</th>
        <th>الدرجات</th>
        <th>معدلات الفصول</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td style="font-weight: 500;">اللغة العربية</td>
        <td style="text-align:center;">__ARABIC__</td>
        <td rowspan="3" class="avg-cell">__AVG1__\\20</td>
      </tr>
      <tr>
        <td style="font-weight: 500;">التربية الإسلامية</td>
        <td style="text-align:center;">__ISLAMIC__</td>
      </tr>
      <tr>
        <td style="font-weight: 500;">الرياضيات</td>
        <td style="text-align:center;">__MATH__</td>
      </tr>
      <tr>
        <td style="font-weight: 500;">الفرنسية</td>
        <td style="text-align:center;">__FRENCH__</td>
        <th style="background:#f1f5f9; color: #1e293b;">الملاحظات</th>
      </tr>
      <tr>
        <td style="font-weight: 500;">العلوم الطبيعية</td>
        <td style="text-align:center;">__SCIENCE__</td>
        <td rowspan="3" class="avg-cell">__AVG2__\\20</td>
      </tr>
      <tr>
        <td style="font-weight: 500;">التاريخ والجغرافيا</td>
        <td style="text-align:center;">__HISTORY__</td>
      </tr>
      <tr>
        <td style="font-weight: 500;">التربية المدنية</td>
        <td style="text-align:center;">__CIVICS__</td>
      </tr>
      <tr>
        <td style="font-weight: 500;">التربية الفنية</td>
        <td style="text-align:center;">__ART__</td>
        <th style="background:#f1f5f9; color: #1e293b;">معدل الامتحان الحالي</th>
      </tr>
      <tr>
        <td style="font-weight: 500;">الرياضة البدنية</td>
        <td style="text-align:center;">__SPORT__</td>
        <td rowspan="4" class="avg-cell">__AVG3__\\20</td>
      </tr>
      <tr>
        <td style="font-weight: bold;">المجموع</td>
        <td style="text-align:center; font-weight: bold;">__TOTAL__\\200</td>
      </tr>
      <tr>
        <td style="font-weight:bold; background: #fff1f2;">المعدل بالفصل</td>
        <td style="text-align:center;font-weight:bold;color:#b91c1c; background: #fff1f2;">__EXAM_AVG__\\20</td>
      </tr>
      <tr>
        <td colspan="2" style="text-align:center; font-size: 14px;">المعدل العام: <strong style="color:#16a34a; font-size: 16px;">__AVG_GENERAL__</strong></td>
      </tr>
      <tr>
        <td colspan="2" style="text-align:center; font-size: 14px; font-weight: bold;">الرتبة: <strong style="font-size: 16px; color:#2563eb;">__RANK__</strong></td>
        <td class="decision-cell">__DECISION__</td>
      </tr>
    </tbody>
  </table>

  <div class="footer-row">
    <div>المعلم: ________________</div>
    <div>المدير: ________________</div>
  </div>
</div>
<script>window.print();</script>
</body>
</html>"""

    # استبدال النصوص والبيانات بشكل آمن
    html = html_template.replace("__LOGO_URL__", logo_url)
    html = html.replace("__DEC_COLOR__", dec_color)
    html = html.replace("__EXAM_TITLE__", exam_title)
    html = html.replace("__STUDENT_NAME__", str(s.get('الاسم', '')))
    html = html.replace("__STUDENT_ID__", str(s.get('الرقم', '')))
    html = html.replace("__ARABIC__", str(format_value(s.get(f'اللغة العربية {suffix}'))))
    html = html.replace("__ISLAMIC__", str(format_value(s.get(f'التربية الاسلامية {suffix}'))))
    html = html.replace("__MATH__", str(format_value(s.get(f'الرياضيات {suffix}'))))
    html = html.replace("__FRENCH__", str(format_value(s.get(f'الفرنسية {suffix}'))))
    html = html.replace("__SCIENCE__", str(format_value(s.get(f'العلوم الطبيعية {suffix}'))))
    html = html.replace("__HISTORY__", str(format_value(s.get(f'التاريخ والجغرافيا {suffix}'))))
    html = html.replace("__CIVICS__", str(format_value(s.get(f'التربية المدنية {suffix}'))))
    html = html.replace("__ART__", str(format_value(s.get(f'التربية الفنية {suffix}'))))
    html = html.replace("__SPORT__", str(format_value(s.get(f'الرياضة البدنية {suffix}'))))
    html = html.replace("__AVG1__", str(avg1))
    html = html.replace("__AVG2__", str(avg2))
    html = html.replace("__AVG3__", str(avg3))
    html = html.replace("__TOTAL__", str(total_val))
    html = html.replace("__EXAM_AVG__", str(exam_avg))
    html = html.replace("__AVG_GENERAL__", str(avg_general))
    html = html.replace("__RANK__", str(rank_val))
    html = html.replace("__DECISION__", str(decision_val))

    return html

# دالة مساعدة لتقريب المعدلات
def format_value(val):
    try:
        return round(float(val), 2)
    except (ValueError, TypeError):
        return val if pd.notna(val) else 'غير متوفر'

# اسم ملف البيانات الثابت
EXCEL_FILE = 'results.xlsx'

if not os.path.exists(EXCEL_FILE):
    st.error("⚠️ ملف النتائج (results.xlsx) غير موجود. يرجى رفعه في GitHub.")
else:
    try:
        df = pd.read_excel(EXCEL_FILE)
        
        # تهيئة الـ Session State لحفظ بيانات الطالب لمنع اختفاء النتائج عند التنقل
        if "student_data" not in st.session_state:
            st.session_state.student_data = None
        if "searched" not in st.session_state:
            st.session_state.searched = False

        # حقل المدخلات للبحث
        query = st.text_input("أدخل رقم التلميذ أو الاسم الكامل:", placeholder="مثال: 10 أو أحمد محمد")
        
        if st.button("استعلام"):
            if query:
                q = str(query).strip()
                match = df[(df['الرقم'].astype(str).str.strip() == q) | 
                           (df['الاسم'].str.strip().str.contains(q, case=False, na=False))]
                
                if not match.empty:
                    st.session_state.student_data = match.iloc[0].to_dict()
                    st.session_state.searched = True
                else:
                    st.session_state.student_data = None
                    st.session_state.searched = True
                    st.error(f"❌ لم يتم العثور على نتيجة لـ '{query}'.")
            else:
                st.info("يرجى كتابة الاسم أو الرقم أولاً.")

        # عرض البيانات في حالة الاستعلام الناجح وحفظها في الجلسة
        if st.session_state.searched and st.session_state.student_data:
            s = st.session_state.student_data
            
            st.divider()
            st.header(f"مرحباً، {s.get('الاسم', 'أيها التلميذ')}")
            st.info(f"رقم التلميذ: {s.get('الرقم', 'غير متوفر')}")

            subjects_list = [
                'اللغة العربية', 'التربية الاسلامية', 'الرياضيات', 'الفرنسية', 
                'العلوم الطبيعية', 'التاريخ والجغرافيا', 'التربية الفنية', 
                'التربية المدنية', 'الرياضة البدنية'
            ]

            tab1, tab2, tab3 = st.tabs(["📝 الامتحان الأول", "📝 الامتحان الثاني", "🏆 الامتحان الأخير"])
            
            # --- خانة الامتحان الأول ---
            with tab1:
                st.subheader("📊 كشف درجات الامتحان الأول")
                labels1 = [sub for sub in subjects_list]
                values1 = [format_value(s.get(f'{sub} 1')) for sub in subjects_list]
                
                labels1.extend(['المجموع', 'معدل الامتحان الأول', 'الرتبة', 'القرار'])
                values1.extend([
                    format_value(s.get('المجموع 1')),
                    format_value(s.get('معدل الامتحان الأول')),
                    s.get('الرتبة 1', 'غير متوفر'),
                    s.get('القرار 1', 'غير متوفر')
                ])
                st.table(pd.DataFrame({'المادة / البيان': labels1, 'النتيجة': values1}))

                report1_html = build_report_html(s, format_value, exam_num=1)
                st.download_button(
                    label="🖨️ تحميل كشف درجات الامتحان الأول للطباعة",
                    data=report1_html,
                    file_name=f"كشف_الامتحان_الأول_{s.get('الاسم')}.html",
                    mime="text/html"
                )

            # --- خانة الامتحان الثاني ---
            with tab2:
                st.subheader("📊 كشف درجات الامتحان الثاني")
                labels2 = [sub for sub in subjects_list]
                values2 = [format_value(s.get(f'{sub} 2')) for sub in subjects_list]
                
                labels2.extend(['المجموع', 'معدل الامتحان الثاني', 'الرتبة', 'القرار'])
                values2.extend([
                    format_value(s.get('المجموع 2')),
                    format_value(s.get('معدل الامتحان الثاني')),
                    s.get('الرتبة 2', 'غير متوفر'),
                    s.get('القرار 2', 'غير متوفر')
                ])
                st.table(pd.DataFrame({'المادة / البيان': labels2, 'النتيجة': values2}))

                report2_html = build_report_html(s, format_value, exam_num=2)
                st.download_button(
                    label="🖨️ تحميل كشف درجات الامتحان الثاني للطباعة",
                    data=report2_html,
                    file_name=f"كشف_الامتحان_الثاني_{s.get('الاسم')}.html",
                    mime="text/html"
                )

            # --- خانة الامتحان الأخير والنهائي ---
            with tab3:
                st.subheader("📊 كشف درجات الامتحان الأخير والنهائي")
                labels3 = [sub for sub in subjects_list]
                values3 = [format_value(s.get(f'{sub} 3')) for sub in subjects_list]
                
                labels3.extend(['المجموع', 'معدل الامتحان الأول', 'معدل الامتحان الثاني', 'معدل الامتحان الأخير', 'المعدل العام', 'الرتبة العامة', 'القرار العام'])
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
                
                report3_html = build_report_html(s, format_value, exam_num=3)
                st.download_button(
                    label="🖨️ تحميل كشف درجات الامتحان النهائي للطباعة",
                    data=report3_html,
                    file_name=f"كشف_الامتحان_النهائي_{s.get('الاسم')}.html",
                    mime="text/html"
                )

                dec_general = str(s.get('القرار العام', ''))
                if "ناجح" in dec_general or "منتقل" in dec_general:
                    st.markdown(f'<div class="success-box">🏆 النتيجة النهائية للعام الدراسي: {dec_general} 🎈</div>', unsafe_allow_html=True)
                    st.balloons()
                elif "راسب" in dec_general or "مكرر" in dec_general:
                    st.markdown(f'<div class="fail-box">😔 النتيجة النهائية للعام الدراسي: {dec_general} 💔</div>', unsafe_allow_html=True)

    except Exception as e:
        st.error(f"حدث خطأ في قراءة البيانات: {e}")
