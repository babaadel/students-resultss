cat > /mnt/user-data/outputs/app.py << 'ENDOFFILE'
import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="بوابة نتائج التلاميذ", page_icon="🎓", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Amiri:wght@400;700&display=swap');

.stApp {
    direction: rtl;
    text-align: right;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background: #f0f2f5;
}
div.stButton > button {
    width: 100%;
    border-radius: 10px;
    background-color: #1a3c5e;
    color: white;
    height: 3.2em;
    font-weight: bold;
    font-size: 16px;
    border: none;
}
div.stButton > button:hover { background-color: #2c6e49; }
button[data-baseweb="tab"] {
    font-size: 15px !important;
    font-weight: bold !important;
    padding: 10px 18px !important;
}
.success-box {
    color: #15803d;
    background-color: #f0fdf4;
    border: 2px solid #4ade80;
    padding: 20px;
    border-radius: 14px;
    text-align: center;
    font-size: 22px;
    font-weight: bold;
    margin: 16px 0;
    font-family: 'Amiri', serif;
}
.fail-box {
    color: #b91c1c;
    background-color: #fef2f2;
    border: 2px solid #fca5a5;
    padding: 20px;
    border-radius: 14px;
    text-align: center;
    font-size: 22px;
    font-weight: bold;
    margin: 16px 0;
    font-family: 'Amiri', serif;
}
.kashf-wrapper {
    border: 3px solid #1a3c5e;
    border-radius: 6px;
    overflow: hidden;
    margin: 20px 0;
    box-shadow: 0 6px 24px rgba(0,0,0,0.13);
    background: #fff;
    direction: rtl;
}
.kashf-header {
    background: linear-gradient(135deg, #1a3c5e 0%, #2c6e49 100%);
    color: white;
    padding: 18px 20px 12px;
    text-align: center;
    border-bottom: 4px solid #f4c842;
}
.kashf-republic {
    font-family: 'Amiri', serif;
    font-size: 20px;
    font-weight: bold;
}
.kashf-ministry { font-size: 13px; opacity: 0.88; margin-top: 3px; }
.kashf-motto {
    color: #f4c842;
    font-size: 13px;
    font-weight: bold;
    letter-spacing: 3px;
    margin-top: 5px;
}
.kashf-exam-title {
    font-family: 'Amiri', serif;
    font-size: 26px;
    font-weight: bold;
    color: #f4c842;
    margin-top: 10px;
}
.kashf-doc-title {
    font-family: 'Amiri', serif;
    font-size: 20px;
    color: #fff;
    opacity: 0.9;
    margin-top: 4px;
    border: 1px solid rgba(244,200,66,0.4);
    display: inline-block;
    padding: 2px 24px;
    border-radius: 4px;
    background: rgba(244,200,66,0.1);
}
.info-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    border-bottom: 2px solid #1a3c5e;
}
.info-cell {
    padding: 10px 16px;
    border-left: 1px solid #dde3ea;
    border-bottom: 1px solid #dde3ea;
    font-size: 14px;
}
.info-label { color: #666; margin-left: 6px; }
.info-value { font-weight: bold; color: #1a3c5e; }

.grades-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 14px;
    direction: rtl;
}
.grades-table th {
    background: #1a3c5e;
    color: white;
    padding: 10px 12px;
    text-align: center;
    border: 1px solid #2c4f72;
    font-weight: bold;
}
.grades-table td {
    padding: 8px 12px;
    border: 1px solid #dde3ea;
    text-align: center;
}
.grades-table td.subj {
    text-align: right;
    font-weight: bold;
    color: #1a3c5e;
    background: #f7f9fb;
    padding-right: 14px;
}
.grades-table td.dark { background: #3a3a3a; }
.grades-table tr:nth-child(even) { background: #f4f7fb; }
.grades-table tr:nth-child(odd)  { background: #fff; }

.avgs-row {
    display: flex;
    border-top: 2px solid #1a3c5e;
    border-bottom: 2px solid #1a3c5e;
    background: #eef2f7;
    flex-wrap: wrap;
}
.avg-box {
    flex: 1;
    min-width: 90px;
    text-align: center;
    padding: 12px 8px;
    border-left: 1px solid #c8d4e0;
}
.avg-label { font-size: 12px; color: #555; margin-bottom: 4px; }
.avg-val-g { font-size: 20px; font-weight: bold; color: #1a7a1a; }
.avg-val-r { font-size: 20px; font-weight: bold; color: #c0392b; }

.summary-row {
    display: flex;
    border-top: 2px solid #1a3c5e;
    flex-wrap: wrap;
    background: #fff;
}
.sum-box {
    flex: 1;
    min-width: 90px;
    text-align: center;
    padding: 12px 8px;
    border-left: 1px solid #d0d8e0;
}
.sum-label { font-size: 12px; color: #666; margin-bottom: 4px; }
.sum-val   { font-size: 18px; font-weight: bold; color: #1a3c5e; }
.sum-avg   { font-size: 18px; font-weight: bold; color: #c0392b; }
.verdict-pass {
    font-family: 'Amiri', serif;
    font-size: 26px;
    font-weight: bold;
    color: #1a7a1a;
}
.verdict-fail {
    font-family: 'Amiri', serif;
    font-size: 26px;
    font-weight: bold;
    color: #c0392b;
}
.sig-row {
    display: flex;
    justify-content: space-between;
    padding: 14px 24px;
    border-top: 1px solid #e0e4ea;
    font-size: 14px;
    color: #444;
    background: #fafbfc;
}
@media (max-width: 600px) {
    .info-grid { grid-template-columns: 1fr; }
    .summary-row, .avgs-row { flex-direction: column; }
    .grades-table { font-size: 12px; }
    .kashf-exam-title { font-size: 20px; }
}
</style>
""", unsafe_allow_html=True)

EXCEL_FILE = 'results.xlsx'

SUBJECTS = [
    ("اللغة العربية",      50),
    ("التربية الإسلامية",  30),
    ("الرياضيات",          40),
    ("الفرنسية",           30),
    ("العلوم الطبيعية",    20),
    ("التاريخ والجغرافيا", 20),
    ("التربية المدنية",    10),
    ("التربية الفنية",     None),
    ("التربية البدنية",    None),
]

def fmt(val, dec=2):
    if val is None or (isinstance(val, float) and pd.isna(val)):
        return "—"
    try:
        return f"{float(val):.{dec}f}"
    except:
        return str(val) if str(val).strip() else "—"

def is_pass(val):
    try:
        return float(val) >= 10
    except:
        return False

def exam_label(n):
    return "الأول" if n == 1 else "الثاني" if n == 2 else "الأخير"

def build_kashf(s, exam_num, show_general=False):
    elabel = exam_label(exam_num)
    suffix = f" {exam_num}"

    avg1 = fmt(s.get('معدل الامتحان الأول',  s.get('معدل الامتحان الاول', '')))
    avg2 = fmt(s.get('معدل الامتحان الثاني', ''))
    avg3 = fmt(s.get('معدل الامتحان الأخير', s.get('معدل الامتحان الثالث', '')))

    html = f"""
    <div class="kashf-wrapper">
      <div class="kashf-header">
        <div class="kashf-republic">الجـمهورية الإسلامية الموريتانية</div>
        <div class="kashf-ministry">وزارة التربية وإصلاح النظام التعليمي</div>
        <div class="kashf-motto">شـرف – إخـاء – عـدل</div>
        <div class="kashf-exam-title">امتحان الفصل {elabel}</div>
        <div class="kashf-doc-title">كشف الدرجات</div>
      </div>
      <div class="info-grid">
        <div class="info-cell">
          <span class="info-label">الاسم الكامل:</span>
          <span class="info-value">{s.get('الاسم', '—')}</span>
        </div>
        <div class="info-cell">
          <span class="info-label">رقم النداء:</span>
          <span class="info-value">{s.get('الرقم', s.get('رقم النداء', '—'))}</span>
        </div>
      </div>
      <table class="grades-table">
        <thead>
          <tr>
            <th>المواد</th>
            <th>الدرجات</th>
          </tr>
        </thead>
        <tbody>
    """

    for label, max_score in SUBJECTS:
        col_key = f"{label}{suffix}"
        score   = s.get(col_key, s.get(label, ''))
        score_str = str(score).strip()
        if max_score and score_str not in ('', 'nan', '—'):
            score_display = f"{fmt(score)}\\{max_score}"
        else:
            score_display = ''
        dark = 'dark' if max_score is None else ''
        html += f'<tr><td class="subj">{label}</td><td class="{dark}">{score_display}</td></tr>'

    html += f"""
        </tbody>
      </table>
      <div class="avgs-row">
        <div class="avg-box">
          <div class="avg-label">معدل الامتحان الأول</div>
          <div class="avg-val-g">{avg1}\\20</div>
        </div>
        <div class="avg-box">
          <div class="avg-label">معدل الامتحان الثاني</div>
          <div class="avg-val-r">{avg2}\\20</div>
        </div>
        <div class="avg-box">
          <div class="avg-label">معدل الامتحان الأخير</div>
          <div class="avg-val-g">{avg3}\\20</div>
        </div>
      </div>
    """

    total_key   = f"المجموع{suffix}"
    avg_key     = f"معدل الامتحان {elabel}"
    rank_key    = f"الرتبة{suffix}"
    verdict_key = f"القرار{suffix}"

    total   = fmt(s.get(total_key, ''))
    avg_val = fmt(s.get(avg_key, ''))
    rank    = s.get(rank_key, s.get('الرتبة', '—'))
    verdict = str(s.get(verdict_key, '')).strip()
    gen_avg = fmt(s.get('المعدل العام', '')) if show_general else None

    passed   = is_pass(s.get(avg_key, s.get('المعدل العام', 0)))
    v_class  = "verdict-pass" if passed else "verdict-fail"
    v_symbol = verdict if verdict else ("ناجح" if passed else "راسب")

    html += '<div class="summary-row">'
    html += f'<div class="sum-box"><div class="sum-label">المجموع</div><div class="sum-val">{total}\\200</div></div>'
    html += f'<div class="sum-box"><div class="sum-label">المعدل</div><div class="sum-avg">{avg_val}\\20</div></div>'
    if show_general and gen_avg:
        html += f'<div class="sum-box"><div class="sum-label">المعدل العام</div><div class="sum-avg">{gen_avg}\\20</div></div>'
    html += f'<div class="sum-box"><div class="sum-label">الرتبة</div><div class="sum-val">{rank}</div></div>'
    html += f'<div class="sum-box"><div class="sum-label">&nbsp;</div><div class="{v_class}">{v_symbol}</div></div>'
    html += '</div>'
    html += '<div class="sig-row"><div>المعلم: _______________</div><div>المدير: _______________</div></div>'
    html += '</div>'
    return html, passed

# ── الواجهة ──
st.markdown("""
<div style="text-align:center; padding:20px 0 10px; direction:rtl;">
  <div style="font-size:40px;">🎓</div>
  <h1 style="color:#1a3c5e; font-family:'Amiri',serif; margin:4px 0;">بوابة نتائج التلاميذ</h1>
  <p style="color:#555; font-size:15px;">استعلم عن نتيجتك باستخدام الاسم أو رقم النداء</p>
</div>
""", unsafe_allow_html=True)

if not os.path.exists(EXCEL_FILE):
    st.error("⚠️ ملف النتائج (results.xlsx) غير موجود.")
    st.info("📌 ضع ملف `results.xlsx` في نفس مجلد `app.py`.")
    st.stop()

try:
    df = pd.read_excel(EXCEL_FILE)
except Exception as e:
    st.error(f"خطأ في قراءة الملف: {e}")
    st.stop()

col1, col2 = st.columns([3, 1])
with col1:
    query = st.text_input("ابحث:", placeholder="رقم النداء أو الاسم...", label_visibility="collapsed")
with col2:
    search = st.button("🔍 استعلام")

if search or query:
    if not query.strip():
        st.info("يرجى كتابة الاسم أو رقم النداء.")
        st.stop()

    q          = str(query).strip()
    name_col   = 'الاسم'      if 'الاسم'      in df.columns else df.columns[1]
    number_col = 'الرقم'      if 'الرقم'      in df.columns else (
                 'رقم النداء' if 'رقم النداء'  in df.columns else df.columns[0])

    match = df[
        (df[number_col].astype(str).str.strip() == q) |
        (df[name_col].astype(str).str.contains(q, case=False, na=False))
    ]

    if match.empty:
        st.error(f"❌ لم يُعثر على «{query}».")
        st.stop()

    s = match.iloc[0].to_dict()
    st.success(f"✅ تم العثور على: **{s.get(name_col,'—')}**")
    st.divider()

    tab1, tab2, tab3 = st.tabs(["📝 الامتحان الأول", "📝 الامتحان الثاني", "🏆 الامتحان الأخير"])

    with tab1:
        html1, _ = build_kashf(s, 1)
        st.markdown(html1, unsafe_allow_html=True)

    with tab2:
        html2, _ = build_kashf(s, 2)
        st.markdown(html2, unsafe_allow_html=True)

    with tab3:
        html3, passed = build_kashf(s, 3, show_general=True)
        st.markdown(html3, unsafe_allow_html=True)

        verdict_g  = str(s.get('القرار العام', '')).strip()
        final_pass = is_pass(s.get('المعدل العام', s.get('معدل الامتحان الأخير', 0)))

        if "ناجح" in verdict_g or "منتقل" in verdict_g or (not verdict_g and final_pass):
            label = verdict_g or "ناجح 🎈"
            st.markdown(f'<div class="success-box">🏆 النتيجة النهائية: {label}</div>', unsafe_allow_html=True)
            st.balloons()
        elif "راسب" in verdict_g or "مكرر" in verdict_g or (not verdict_g and not final_pass):
            label = verdict_g or "راسب"
            st.markdown(f'<div class="fail-box">😔 النتيجة النهائية: {label}</div>', unsafe_allow_html=True)
ENDOFFILE
