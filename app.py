import streamlit as st
import pandas as pd
import os
import base64

st.set_page_config(page_title="منصة نتائج التلاميذ", page_icon="🎓", layout="centered")

LOGO_B64 = "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MmFYUjVJbjA9AABRDBQAAABTYW1zdW5nX0NhcHR1cmVfSW5mb1NjcmVlbnNob3QAAKELGAAAAFBob3RvRWRpdG9yX1JlX0VkaXRfRGF0YXsib3JpZ2luYWxQYXRoIjoiXC9kYXRhXC9zZWNcL3Bob3RvZWRpdG9yXC8wXC9jNTgxYWJlNWUzMTliNmZjNmZkY2MyNzM2YzUzMGU1ODQ5NDhkNzJkYTY5NGIwZThmNDU1YjNkMzZlMjdjYzk2XzUwNTYwOC5qcGciLCJyZXByZXNlbnRhdGl2ZUZyYW1lTG9jIjotMSwic3RhcnRNb3Rpb25WaWRlbyI6LTEsImVuZE1vdGlvblZpZGVvIjotMSwiaXNNb3Rpb25WaWRlb011dGUiOmZhbHNlLCJpc1RyaW1Nb3Rpb25WaWRlbyI6ZmFsc2UsImNsaXBJbmZvVmFsdWUiOiJ7XCJtQ2VudGVyWFwiOjAuNTIwNTMzNTYxNzA2NTQzLFwibUNlbnRlcllcIjowLjE0NjM5ODA5NzI3NjY4NzYyLFwibVdpZHRoXCI6MC4yMzQ3MzczNTE1MzY3NTA4LFwibUhlaWdodFwiOjAuMTMyNjkzNDI0ODIwODk5OTYsXCJtUm90YXRpb25cIjowLFwibVJvdGF0ZVwiOjAsXCJtSEZsaXBcIjowLFwibVZGbGlwXCI6MCxcIm1Sb3RhdGlvbkVmZmVjdFwiOjAsXCJtUm90YXRlRWZmZWN0XCI6MCxcIm1IRmxpcEVmZmVjdFwiOjAsXCJtVkZsaXBFZmZlY3RcIjowLFwibUhvelBlcnNwZWN0aXZlXCI6MCxcIm1WZXJQZXJzcGVjdGl2ZVwiOjB9IiwidG9uZVZhbHVlIjoie1wiYnJpZ2h0bmVzc1wiOjEwMCxcImV4cG9zdXJlXCI6MTAwLFwiY29udHJhc3RcIjoxMDAsXCJzYXR1cmF0aW9uXCI6MTAwLFwiaHVlXCI6MTAwLFwid2JNb2RlXCI6LTEsXCJ3YlRlbXBlcmF0dXJlXCI6MTAwLFwidGludFwiOjEwMCxcInNoYWRvd1wiOjEwMCxcImhpZ2hsaWdodFwiOjEwMCxcImxpZ2h0YmFsYW5jZVwiOjEwMCxcInNoYXJwbmVzc1wiOjEwMCxcImRlZmluaXRpb25cIjoxMDAsXCJpc0JyaWdodG5lc3NJUEVcIjpmYWxzZSxcImlzRXhwb3N1cmVJUEVcIjpmYWxzZSxcImlzQ29udHJhc3RJUEVcIjpmYWxzZSxcImlzU2F0dXJhdGlvbklQRVwiOmZhbHNlfSIsImVmZmVjdFZhbHVlIjoie1wiZmlsdGVySW5kaWNhdGlvblwiOjQwOTcsXCJhbHBoYVZhbHVlXCI6MTAwLFwiZmlsdGVyVHlwZVwiOjB9IiwicG9ydHJhaXRFZmZlY3RWYWx1ZSI6IntcImVmZmVjdElkXCI6LTEsXCJlZmZlY3RMZXZlbFwiOi0xLFwiZXhpZlJvdGF0aW9uXCI6MCxcImxpZ2h0TGV2ZWxcIjowLFwidG91Y2hYXCI6MCxcInRvdWNoWVwiOjAsXCJyZWZvY3VzWFwiOi0xLFwicmVmb2N1c1lcIjotMSxcImVmZmVjdElkT3JpZ2luYWxcIjotMSxcImVmZmVjdExldmVsT3JpZ2luYWxcIjotMSxcImxpZ2h0TGV2ZWxPcmlnaW5hbFwiOi0xLFwidG91Y2hYT3JpZ2luYWxcIjowLFwidG91Y2hZT3JpZ2luYWxcIjowLFwicmVmb2N1c1hPcmlnaW5hbFwiOi0xLFwicmVmb2N1c1lPcmlnaW5hbFwiOi0xLFwid2F0ZXJNYXJrUmVtb3ZlZFwiOmZhbHNlLFwid2F0ZXJNYXJrUmVtb3ZlZE9yaWdpbmFsXCI6ZmFsc2V9IiwiaXNCbGVuZGluZyI6dHJ1ZSwiaXNOb3RSZUVkaXQiOmZhbHNlLCJzZXBWZXJzaW9uIjoiMTcwMDAwIiwibmRlVmVyc2lvbiI6MSwicmVTaXplIjo0LCJpc1NjYWxlQUkiOmZhbHNlLCJyb3RhdGlvbiI6MSwiYWRqdXN0bWVudFZhbHVlIjoie1wibUNyb3BTdGF0ZVwiOjEzMTA3Nn0iLCJpc0FwcGx5U2hhcGVDb3JyZWN0aW9uIjpmYWxzZSwiaXNOZXdSZUVkaXRPbmx5IjpmYWxzZSwiaXNEZWNvUmVFZGl0T25seSI6ZmFsc2UsImlzQUlGaWx0ZXJSZUVkaXRPbmx5IjpmYWxzZX0AAKELFgAAAE9yaWdpbmFsX1BhdGhfSGFzaF9LZXk3YmQ1YTc1NjIwZDUzZDE5MWE4NzY0NTA2NDU2YTNlMTQ0ZjFlMThkM2M4MzdmNjk1M2NhZmJkYWUwMjYxM2VmLzUwNTYwOFNFRkhrAAAABAAAAAAAoQ2ZBwAAgQAAAAAAUQwYBwAAJgAAAAAAoQvyBgAAjQYAAAAAoQtlAAAAZQAAADwAAABTRUZU"
LOGO_URI = f"data:image/jpeg;base64,{LOGO_B64}"

st.markdown("""
    <style>
    .stApp { direction: rtl; text-align: right; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    div.stButton > button { width: 100%; border-radius: 12px; background-color: #2563eb; color: white; height: 3.2em; font-weight: bold; font-size: 16px; border: none; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); }
    div.stButton > button:hover { background-color: #1d4ed8; }
    button[data-baseweb="tab"] { font-size: 16px !important; font-weight: bold !important; padding: 12px 20px !important; }
    .success-box { color: #15803d; background-color: #f0fdf4; border: 1px solid #bbf7d0; padding: 18px; border-radius: 14px; text-align: center; font-size: 18px; font-weight: bold; margin: 15px 0; }
    .fail-box { color: #b91c1c; background-color: #fef2f2; border: 1px solid #fecaca; padding: 18px; border-radius: 14px; text-align: center; font-size: 18px; font-weight: bold; margin: 15px 0; }
    .stTable { width: 100% !important; border-radius: 10px; overflow: hidden; }
    .portal-header {
        background: linear-gradient(160deg, #0a3d1f 0%, #1a6b38 50%, #0a3d1f 100%);
        color: white; border-radius: 16px; padding: 20px 18px 14px;
        margin-bottom: 20px;
        border: 3px double #c9a227;
        text-align: center;
        box-shadow: 0 6px 24px rgba(0,0,0,0.3);
    }
    .portal-header img { width: 90px; height: 90px; object-fit: contain; border-radius: 50%; border: 3px solid #c9a227; margin-bottom: 8px; }
    .portal-header h1 { font-size: 17px; font-weight: bold; margin: 4px 0; letter-spacing: 0.5px; }
    .portal-header h2 { font-size: 13px; font-weight: normal; margin: 3px 0; opacity: 0.88; }
    .portal-header .motto { font-size: 13px; color: #f0c040; font-weight: bold; margin-top: 8px; letter-spacing: 3px; }
    .portal-header .divider { border: 1px solid rgba(201,162,39,0.5); margin: 8px 0; }
    .print-link-btn {
        display: block; width: 100%; padding: 13px;
        background: linear-gradient(90deg, #15803d, #16a34a);
        color: white !important; border: none; border-radius: 10px;
        font-size: 15px; font-weight: bold;
        text-align: center; text-decoration: none !important;
        margin: 10px 0; cursor: pointer;
        font-family: \'Segoe UI\', Tahoma, sans-serif;
        box-shadow: 0 3px 8px rgba(0,0,0,0.15);
    }
    .print-link-btn:hover { background: linear-gradient(90deg, #166534, #15803d); }
    </style>
    """, unsafe_allow_html=True)

st.markdown(f"""
<div class="portal-header">
    <img src="{LOGO_URI}" alt="شعار موريتانيا">
    <h1>الجمهورية الإسلامية الموريتانية</h1>
    <hr class="divider">
    <h2>وزارة التربية وإصلاح النظام التعليمي</h2>
    <div class="motto">شـرف &nbsp;•&nbsp; إخـاء &nbsp;•&nbsp; عـدالة</div>
</div>
""", unsafe_allow_html=True)

st.title("🎓 بوابة نتائج التلاميذ")
st.write("استخدم الاسم أو الرقم للاستعلام عن النتيجة")

EXCEL_FILE = 'results.xlsx'

def build_report_html(s, subjects_list, format_value, exam_num, logo_b64):
    logo_uri = f"data:image/jpeg;base64,{logo_b64}"
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

    def subj(name):
        return format_value(s.get(f'{name} {suffix}'))

    html = f"""<!DOCTYPE html>
<html dir="rtl" lang="ar">
<head>
<meta charset="UTF-8">
<title>كشف درجات - {s.get('الاسم','')}</title>
<style>
  * {{ box-sizing:border-box; margin:0; padding:0; }}
  body {{ font-family:'Traditional Arabic','Segoe UI',Tahoma,sans-serif; direction:rtl; background:#f5f0e8; color:#111; padding:20px; }}
  .page {{ background:white; max-width:780px; margin:auto; border:4px double #8b6914; box-shadow:0 0 0 8px #f5f0e8, 0 0 0 12px #8b6914; padding:16px; }}
  /* ترويسة */
  .top {{ display:flex; justify-content:space-between; align-items:center; border-bottom:3px double #8b6914; padding-bottom:12px; margin-bottom:10px; gap:6px; }}
  .col {{ font-size:13px; line-height:2; }}
  .col-c {{ text-align:center; }}
  .col-c img {{ width:95px; height:95px; object-fit:contain; border-radius:50%; border:3px solid #8b6914; }}
  .col-c .rep {{ font-size:9px; color:#777; margin-top:3px; font-style:italic; }}
  .col-l {{ text-align:left; }}
  .motto-line {{ font-size:11px; color:#8b6914; font-weight:bold; margin-bottom:3px; }}
  /* عنوان الامتحان */
  .exam-title {{ text-align:center; font-size:24px; font-weight:bold; margin:12px 0 6px; color:#1a1a1a; border-bottom:2px solid #c9a227; padding-bottom:6px; }}
  /* شريط كشف الدرجات */
  .kashf-wrap {{ text-align:center; margin:8px 0 12px; }}
  .kashf {{
    display:inline-block; padding:7px 36px; font-size:20px; font-weight:bold;
    background:linear-gradient(135deg,#d4edda,#a8d5b5);
    border:2px solid #5a9e6f; border-radius:8px;
    box-shadow:2px 2px 6px rgba(0,0,0,0.1);
    color:#1a4a2a; letter-spacing:2px;
  }}
  /* معلومات الطالب */
  .sinfo {{
    display:flex; justify-content:space-between;
    background:linear-gradient(90deg,#f8f4e8,#fdf9f0,#f8f4e8);
    border:1px solid #c9a227; border-radius:6px;
    padding:8px 14px; font-size:13px; margin:10px 0;
  }}
  .sinfo span {{ font-weight:bold; color:#1a56db; }}
  /* الجدول */
  table {{ width:100%; border-collapse:collapse; font-size:13px; margin-top:8px; }}
  th {{
    background:linear-gradient(180deg,#2c5f3a,#1a4a2a);
    color:white; border:1px solid #1a4a2a; padding:9px 10px;
    text-align:center; font-size:13px;
  }}
  td {{ border:1px solid #aaa; padding:7px 10px; }}
  tr:nth-child(even) td {{ background:#fafff8; }}
  tr:hover td {{ background:#f0fff4; }}
  .ac {{ text-align:center; }}
  .avgc {{
    text-align:center; font-weight:bold; color:#c00;
    font-size:16px; vertical-align:middle;
    background:linear-gradient(180deg,#fff8f0,#fff0e0) !important;
  }}
  .notesc {{
    text-align:center; vertical-align:middle;
    background:#fffff0 !important; color:#555;
    font-style:italic; font-size:12px;
  }}
  .decc {{
    text-align:center; font-weight:bold; font-size:24px;
    color:{dec_color}; vertical-align:middle;
    background:linear-gradient(180deg,#f0fff4,#e0ffe8) !important;
    padding:12px !important;
  }}
  .total-row td {{ background:#f0f8ff !important; font-weight:bold; }}
  .avg-row td {{ background:#fff8e0 !important; font-weight:bold; color:#c00; }}
  /* ذيل */
  .foot {{
    display:flex; justify-content:space-between; margin-top:24px;
    font-size:14px; font-weight:bold;
    border-top:2px double #8b6914; padding-top:12px;
  }}
  /* زخرفة الإطار */
  .corner-deco {{ text-align:center; color:#c9a227; font-size:11px; margin-top:8px; letter-spacing:2px; }}
  @media print {{ body {{ padding:4px; background:white; }} .no-print {{ display:none; }} }}
</style>
</head>
<body>
<div class="page">

  <div class="top">
    <div class="col">
      <strong>الجمهورية الإسلامية الموريتانية</strong><br>
      وزارة التربية وإصلاح النظام التعليمي<br>
      الإدارة الجهوية بولاية لعصابه<br>
      مفتشية التعليم بمقاطعة كنكوصة
    </div>
    <div class="col col-c">
      <img src="{logo_uri}" alt="شعار موريتانيا">
      <div class="rep">REPUBLIQUE ISLAMIQUE DE MAURITANIE</div>
    </div>
    <div class="col col-l">
      <div class="motto-line">شـرف – إخـاء – عـدل</div>
      <strong>العام الدراسي: 2025/2026</strong><br>
      المدرسة: كنكوصة 4<br>
      القسم: الثالث ابتدائي
    </div>
  </div>

  <div class="exam-title">{exam_title}</div>
  <div class="kashf-wrap"><div class="kashf">كـشـف الـدرجـات</div></div>

  <div class="sinfo">
    <div>الاسم الكامل: <span>{s.get('الاسم','')}</span></div>
    <div>الرقم المدرسي: <span>{s.get('الرقم','')}</span></div>
    <div>رقم النداء: <span>{s.get('الرقم','')}</span></div>
  </div>

  <table>
    <thead>
      <tr><th>المواد</th><th>الدرجات</th><th>معدل الامتحان الأول</th></tr>
    </thead>
    <tbody>
      <tr><td>اللغة العربية</td><td class="ac">{subj('اللغة العربية')}</td><td rowspan="3" class="avgc">{avg1}\20</td></tr>
      <tr><td>التربية الإسلامية</td><td class="ac">{subj('التربية الاسلامية')}</td></tr>
      <tr><td>الرياضيات</td><td class="ac">{subj('الرياضيات')}</td></tr>
      <tr><td>الفرنسية</td><td class="ac">{subj('الفرنسية')}</td><th>الملاحظات</th></tr>
      <tr><td>العلوم الطبيعية</td><td class="ac">{subj('العلوم الطبيعية')}</td><td rowspan="3" class="avgc">{avg2}\20</td></tr>
      <tr><td>التاريخ والجغرافيا</td><td class="ac">{subj('التاريخ والجغرافيا')}</td></tr>
      <tr><td>التربية المدنية</td><td class="ac">{subj('التربية المدنية')}</td></tr>
      <tr><td>التربية الفنية</td><td class="ac">{subj('التربية الفنية')}</td><th>معدل الامتحان الثالث</th></tr>
      <tr><td>الرياضة البدنية</td><td class="ac">{subj('الرياضة البدنية')}</td><td rowspan="4" class="avgc">{avg3}\20</td></tr>
      <tr class="total-row"><td>المجموع</td><td class="ac">{total_val}\200</td></tr>
      <tr class="avg-row"><td><strong>المعدل</strong></td><td class="ac">{exam_avg}\20</td></tr>
      <tr><td colspan="2" class="ac" style="background:#f0f8ff;">المعدل العام: <strong style="color:#16a34a;font-size:15px;">{avg_general}</strong></td></tr>
      <tr><td colspan="2" class="ac" style="background:#f8f8f0;">الرتبة: <strong>{rank_val}</strong></td><td class="decc">{decision_val}</td></tr>
    </tbody>
  </table>

  <div class="foot">
    <div>المعلم: ____________________</div>
    <div>المدير: ____________________</div>
  </div>
  <div class="corner-deco">✦ ✦ ✦ وفقك الله ✦ ✦ ✦</div>
</div>
</body>
</html>"""
    return html


def make_print_link(html_content, label):
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
                            labels1.append(sub); values1.append(format_value(s.get(f'{sub} 1')))
                        labels1.extend(['المجموع','معدل الامتحان الأول','الرتبة','القرار'])
                        values1.extend([format_value(s.get('المجموع 1')),format_value(s.get('معدل الامتحان الأول')),s.get('الرتبة 1','غير متوفر'),s.get('القرار 1','غير متوفر')])
                        st.table(pd.DataFrame({'المادة / البيان': labels1, 'النتيجة': values1}))
                        r1 = build_report_html(s, subjects_list, format_value, 1, LOGO_B64)
                        st.markdown(make_print_link(r1, "طباعة الشكلية الرسمية — الامتحان الأول"), unsafe_allow_html=True)

                    with tab2:
                        st.subheader("📊 كشف درجات الامتحان الثاني")
                        labels2, values2 = [], []
                        for sub in subjects_list:
                            labels2.append(sub); values2.append(format_value(s.get(f'{sub} 2')))
                        labels2.extend(['المجموع','معدل الامتحان الثاني','الرتبة','القرار'])
                        values2.extend([format_value(s.get('المجموع 2')),format_value(s.get('معدل الامتحان الثاني')),s.get('الرتبة 2','غير متوفر'),s.get('القرار 2','غير متوفر')])
                        st.table(pd.DataFrame({'المادة / البيان': labels2, 'النتيجة': values2}))
                        r2 = build_report_html(s, subjects_list, format_value, 2, LOGO_B64)
                        st.markdown(make_print_link(r2, "طباعة الشكلية الرسمية — الامتحان الثاني"), unsafe_allow_html=True)

                    with tab3:
                        st.subheader("📊 كشف درجات الامتحان الأخير والنهائي")
                        labels3, values3 = [], []
                        for sub in subjects_list:
                            labels3.append(sub); values3.append(format_value(s.get(f'{sub} 3')))
                        labels3.extend(['المجموع','معدل الامتحان الأول','معدل الامتحان الثاني','معدل الامتحان الأخير','المعدل العام','الرتبة العامة','القرار العام'])
                        values3.extend([format_value(s.get('المجموع 3')),format_value(s.get('معدل الامتحان الأول')),format_value(s.get('معدل الامتحان الثاني')),format_value(s.get('معدل الامتحان الأخير')),format_value(s.get('المعدل العام')),s.get('الرتبة العامة','غير متوفر'),s.get('القرار العام','غير متوفر')])
                        st.table(pd.DataFrame({'المادة / البيان': labels3, 'النتيجة': values3}))
                        r3 = build_report_html(s, subjects_list, format_value, 3, LOGO_B64)
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
