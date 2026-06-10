import streamlit as st
import pandas as pd
import os
import base64

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة نتائج التلاميذ", page_icon="🎓", layout="centered")

# 2. CSS
st.markdown("""
    <style>
    .stApp { direction: rtl; text-align: right; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }

    /* ===== ترويسة البوابة ===== */
    .portal-header {
        background: linear-gradient(135deg, #006233 0%, #009639 60%, #006233 100%);
        color: white; border-radius: 14px; padding: 18px 20px;
        margin-bottom: 18px; border: 3px solid #FFD700;
        text-align: center;
    }
    .portal-header .flag { font-size: 52px; margin-bottom: 4px; }
    .portal-header h1 { font-size: 18px; font-weight: bold; margin: 4px 0; letter-spacing: 0.5px; }
    .portal-header h2 { font-size: 14px; font-weight: normal; margin: 3px 0; opacity: 0.9; }
    .portal-header .motto {
        font-size: 13px; color: #FFD700; font-weight: bold;
        margin-top: 6px; letter-spacing: 2px;
    }
    .portal-divider { border: 1px solid rgba(255,255,255,0.3); margin: 8px 0; }

    /* زر الاستعلام */
    div.stButton > button { width: 100%; border-radius: 12px; background-color: #2563eb; color: white; height: 3.2em; font-weight: bold; font-size: 16px; border: none; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); }
    div.stButton > button:hover { background-color: #1d4ed8; }

    button[data-baseweb="tab"] { font-size: 16px !important; font-weight: bold !important; padding: 12px 20px !important; }

    .success-box { color: #15803d; background-color: #f0fdf4; border: 1px solid #bbf7d0; padding: 18px; border-radius: 14px; text-align: center; font-size: 18px; font-weight: bold; margin: 15px 0; }
    .fail-box { color: #b91c1c; background-color: #fef2f2; border: 1px solid #fecaca; padding: 18px; border-radius: 14px; text-align: center; font-size: 18px; font-weight: bold; margin: 15px 0; }
    .stTable { width: 100% !important; border-radius: 10px; overflow: hidden; }

    /* زر الطباعة */
    .print-link-btn {
        display: block; width: 100%; padding: 13px;
        background-color: #16a34a; color: white !important;
        border: none; border-radius: 10px;
        font-size: 15px; font-weight: bold;
        text-align: center; text-decoration: none !important;
        margin: 10px 0; cursor: pointer;
        font-family: 'Segoe UI', Tahoma, sans-serif;
    }
    .print-link-btn:hover { background-color: #15803d; }
    </style>
    """, unsafe_allow_html=True)

# ===== ترويسة البوابة الرسمية =====
st.markdown("""
<div class="portal-header">
    <div class="flag">🇲🇷</div>
    <h1>الجمهورية الإسلامية الموريتانية</h1>
    <hr class="portal-divider">
    <h2>وزارة التربية وإصلاح النظام التعليمي</h2>
    <div class="motto">شـرف &nbsp;•&nbsp; إخـاء &nbsp;•&nbsp; عـدالة</div>
</div>
""", unsafe_allow_html=True)

st.title("🎓 بوابة نتائج التلاميذ")
st.write("استخدم الاسم أو الرقم للاستعلام عن النتيجة")

EXCEL_FILE = 'results.xlsx'

# ===== دالة توليد HTML الشكلية الرسمية =====
def build_report_html(s, subjects_list, format_value, exam_num):
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

    dec_color = "#16a34a" if ("ناجح" in decision_val or "منتقل" in decision_val) else "#dc2626"

    html = f"""<!DOCTYPE html>
<html dir="rtl" lang="ar">
<head>
<meta charset="UTF-8">
<title>كشف درجات - {s.get('الاسم','')}</title>
<style>
  * {{ box-sizing:border-box; margin:0; padding:0; }}
  body {{ font-family:'Traditional Arabic','Segoe UI',Tahoma,sans-serif; direction:rtl; background:white; color:#111; padding:16px; }}
  .outer {{ border:3px solid #000; padding:10px; max-width:760px; margin:auto; }}
  .top {{ display:flex; justify-content:space-between; align-items:center; border-bottom:2px solid #000; padding-bottom:10px; margin-bottom:10px; gap:8px; }}
  .col {{ font-size:13px; line-height:2; }}
  .col-c {{ text-align:center; }}
  .col-c .flag {{ font-size:50px; }}
  .col-c .rep {{ font-size:9px; color:#555; margin-top:2px; }}
  .col-l {{ text-align:left; }}
  .motto {{ font-size:11px; color:#555; margin-bottom:2px; }}
  .exam-title {{ text-align:center; font-size:22px; font-weight:bold; margin:10px 0 5px; }}
  .kashf {{ text-align:center; background:#d4edda; border:1px solid #aaa; border-radius:6px; font-size:19px; font-weight:bold; padding:5px 24px; display:inline-block; margin:6px auto; }}
  .kashf-wrap {{ text-align:center; margin-bottom:10px; }}
  .sinfo {{ display:flex; justify-content:space-between; font-size:13px; margin:8px 4px; }}
  .sinfo span {{ font-weight:bold; color:#1a56db; }}
  table {{ width:100%; border-collapse:collapse; font-size:13px; margin-top:6px; }}
  th {{ background:#f0f0f0; border:1px solid #333; padding:7px 10px; text-align:center; }}
  td {{ border:1px solid #333; padding:6px 10px; }}
  .ac {{ text-align:center; }}
  .avgc {{ text-align:center; font-weight:bold; color:#c00; font-size:15px; vertical-align:middle; }}
  .decc {{ text-align:center; font-weight:bold; font-size:22px; color:{dec_color}; vertical-align:middle; }}
  .foot {{ display:flex; justify-content:space-between; margin-top:22px; font-size:14px; font-weight:bold; border-top:1px solid #aaa; padding-top:10px; }}
  @media print {{ body {{ padding:6px; }} .no-print {{ display:none; }} }}
</style>
</head>
<body>
<div class="outer">
  <div class="top">
    <div class="col">
      <strong>الجمهورية الإسلامية الموريتانية</strong><br>
      وزارة التربية وإصلاح النظام التعليمي<br>
      الإدارة الجهوية بولاية لعصابه<br>
      مفتشية التعليم بمقاطعة كنكوصة
    </div>
    <div class="col col-c">
      <div class="flag">🇲🇷</div>
      <div class="rep">REPUBLIQUE ISLAMIQUE DE MAURITANIE</div>
    </div>
    <div class="col col-l">
      <div class="motto">شـرف – إخـاء – عـدل</div>
      <strong>العام الدراسي: 2025\2026</strong><br>
      المدرسة: كنكوصة 4<br>
      القسم: الثالث ابتدائي
    </div>
  </div>

  <div class="exam-title">{exam_title}</div>
  <div class="kashf-wrap"><div class="kashf">كشف الدرجات</div></div>

  <div class="sinfo">
    <div>الاسم الكامل: <span>{s.get('الاسم','')}</span></div>
    <div>الرقم المدرسي: <span>{s.get('الرقم','')}</span></div>
    <div>رقم النداء: <span>{s.get('الرقم','')}</span></div>
  </div>

  <table>
    <thead>
      <tr>
        <th>المواد</th>
        <th>الدرجات</th>
        <th>معدل الامتحان الأول</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>اللغة العربية</td>
        <td class="ac">{format_value(s.get(f'اللغة العربية {suffix}'))}</td>
        <td rowspan="3" class="avgc">{avg1}\20</td>
      </tr>
      <tr>
        <td>التربية الإسلامية</td>
        <td class="ac">{format_value(s.get(f'التربية الاسلامية {suffix}'))}</td>
      </tr>
      <tr>
        <td>الرياضيات</td>
        <td class="ac">{format_value(s.get(f'الرياضيات {suffix}'))}</td>
      </tr>
      <tr>
        <td>الفرنسية</td>
        <td class="ac">{format_value(s.get(f'الفرنسية {suffix}'))}</td>
        <th>الملاحظات</th>
      </tr>
      <tr>
        <td>العلوم الطبيعية</td>
        <td class="ac">{format_value(s.get(f'العلوم الطبيعية {suffix}'))}</td>
        <td rowspan="3" class="avgc">{avg2}\20</td>
      </tr>
      <tr>
        <td>التاريخ والجغرافيا</td>
        <td class="ac">{format_value(s.get(f'التاريخ والجغرافيا {suffix}'))}</td>
      </tr>
      <tr>
        <td>التربية المدنية</td>
        <td class="ac">{format_value(s.get(f'التربية المدنية {suffix}'))}</td>
      </tr>
      <tr>
        <td>التربية الفنية</td>
        <td class="ac">{format_value(s.get(f'التربية الفنية {suffix}'))}</td>
        <th>معدل الامتحان الثالث</th>
      </tr>
      <tr>
        <td>الرياضة البدنية</td>
        <td class="ac">{format_value(s.get(f'الرياضة البدنية {suffix}'))}</td>
        <td rowspan="4" class="avgc">{avg3}\20</td>
      </tr>
      <tr>
        <td>المجموع</td>
        <td class="ac">{total_val}\200</td>
      </tr>
      <tr>
        <td><strong>المعدل</strong></td>
        <td class="ac" style="font-weight:bold;color:#c00;">{exam_avg}\20</td>
      </tr>
      <tr>
        <td colspan="2" class="ac">المعدل العام: <strong style="color:#16a34a;">{avg_general}</strong></td>
      </tr>
      <tr>
        <td colspan="2" class="ac">الرتبة: <strong>{rank_val}</strong></td>
        <td class="decc">{decision_val}</td>
      </tr>
    </tbody>
  </table>

  <div class="foot">
    <div>المعلم: ________________</div>
    <div>المدير: ________________</div>
  </div>
</div>
</body>
</html>"""
    return html


def make_print_link(html_content, label):
    """تحويل HTML إلى رابط data URI قابل للفتح مباشرة"""
    b64 = base64.b64encode(html_content.encode('utf-8')).decode()
    href = f"data:text/html;base64,{b64}"
    return f'<a class="print-link-btn" href="{href}" target="_blank">🖨️ {label}</a>'


if not os.path.exists(EXCEL_FILE):
    st.error("⚠️ ملف النتائج (results.xlsx) غير موجود. يرجى رفعه في GitHub.")
else:
    try:
        df = pd.read_excel(EXCEL_FILE)

        query = st.text_input("أدخل رقم التلميذ أو الاسم الكامل:", placeholder="مثال: 10 أو أحمد محمد")

        if st.button("استعلام"):
            if query:
                q = str(query).strip()
                match = df[(df['الرقم'].astype(str).str.strip() == q) |
                           (df['الاسم'].str.strip().str.contains(q, case=False, na=False))]

                if not match.empty:
                    s = match.iloc[0].to_dict()

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

                    tab1, tab2, tab3 = st.tabs(["📝 الامتحان الأول", "📝 الامتحان الثاني", "🏆 الامتحان الأخير"])

                    with tab1:
                        st.subheader("📊 كشف درجات الامتحان الأول")
                        labels1, values1 = [], []
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
                        # زر الطباعة
                        r1 = build_report_html(s, subjects_list, format_value, 1)
                        st.markdown(make_print_link(r1, "طباعة الشكلية الرسمية — الامتحان الأول"), unsafe_allow_html=True)

                    with tab2:
                        st.subheader("📊 كشف درجات الامتحان الثاني")
                        labels2, values2 = [], []
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
                        # زر الطباعة
                        r2 = build_report_html(s, subjects_list, format_value, 2)
                        st.markdown(make_print_link(r2, "طباعة الشكلية الرسمية — الامتحان الثاني"), unsafe_allow_html=True)

                    with tab3:
                        st.subheader("📊 كشف درجات الامتحان الأخير والنهائي")
                        labels3, values3 = [], []
                        for sub in subjects_list:
                            labels3.append(sub)
                            values3.append(format_value(s.get(f'{sub} 3')))
                        labels3.extend([
                            'المجموع', 'معدل الامتحان الأول', 'معدل الامتحان الثاني',
                            'معدل الامتحان الأخير', 'المعدل العام', 'الرتبة العامة', 'القرار العام'
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
                        # زر الطباعة
                        r3 = build_report_html(s, subjects_list, format_value, 3)
                        st.markdown(make_print_link(r3, "طباعة الشكلية الرسمية — الامتحان الأخير"), unsafe_allow_html=True)

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
