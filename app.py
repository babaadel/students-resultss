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

/* ── زر البحث ── */
div.stButton > button {
    width: 100%;
    border-radius: 10px;
    background-color: #1a3c5e;
    color: white;
    height: 3.2em;
    font-weight: bold;
    font-size: 16px;
    border: none;
    box-shadow: 0 4px 10px rgba(0,0,0,0.15);
    transition: background 0.2s;
}
div.stButton > button:hover { background-color: #2c6e49; }

/* ── التبويبات ── */
button[data-baseweb="tab"] {
    font-size: 15px !important;
    font-weight: bold !important;
    padding: 10px 18px !important;
}

/* ── رسائل النجاح والرسوب ── */
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

/* ── بطاقة الكشف الرسمي ── */
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
    letter-spacing: 1px;
}
.kashf-ministry {
    font-size: 13px;
    opacity: 0.88;
    margin-top: 3px;
}
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

/* ── معلومات الطالب ── */
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

/* ── جدول الدرجات ── */
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
.grades-table td.subject-name {
    text-align: right;
    font-weight: bold;
    color: #1a3c5e;
    background: #f7f9fb;
    padding-right: 14px;
}
.grades-table td.dark-cell {
    background: #3a3a3a;
}
.grades-table tr:nth-child(even) { background: #f4f7fb; }
.grades-table tr:nth-child(odd)  { background: #fff; }

/* ── سطر الملخص ── */
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
    margin-top: 4px;
}
.verdict-fail {
    font-family: 'Amiri', serif;
    font-size: 26px;
    font-weight: bold;
    color: #c0392b;
    margin-top: 4px;
}

/* ── توقيعات ── */
.sig-row {
    display: flex;
    justify-content: space-between;
    padding: 14px 24px;
    border-top: 1px solid #e0e4ea;
    font-size: 14px;
    color: #444;
    background: #fafbfc;
}

/* ── تجاوب الهاتف ── */
@media (max-width: 600px) {
    .info-grid { grid-template-columns: 1fr; }
    .summary-row { flex-direction: column; }
    .grades-table { font-size: 12px; }
    .kashf-exam-title { font-size: 20px; }
    .sum-box { min-width: 80px; }
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
EXCEL_FILE = 'results.xlsx'

SUBJECTS = [
    ("اللغة العربية",       "arabic",  50),
    ("التربية الإسلامية",   "islamic", 30),
    ("الرياضيات",           "math",    40),
    ("الفرنسية",            "french",  30),
    ("العلوم الطبيعية",     "science", 20),
    ("التاريخ والجغرافيا",  "history", 20),
    ("التربية المدنية",     "civic",   10),
    ("التربية الفنية",      "art",     None),
    ("التربية البدنية",     "sport",   None),
]

def fmt(val, dec=2):
    if val is None or (isinstance(val, float) and pd.isna(val)):
        return "—"
    try:
        return f"{float(val):.{dec}f}"
    except:
        return str(val) if val else "—"

def is_pass(val):
    try:
        return float(val) >= 10
    except:
        return False

def build_kashf(s, exam_num, subjects, show_general=False):
    """يبني HTML كشف الدرجات لامتحان محدد"""

    # ── رأس الكشف ──
    html = """
    <div class="kashf-wrapper">
      <div class="kashf-header">
        <div class="kashf-republic">الجـمهورية الإسلامية الموريتانية</div>
        <div class="kashf-ministry">وزارة التربية وإصلاح النظام التعليمي</div>
        <div class="kashf-motto">شـرف – إخـاء – عـدل</div>
        <div class="kashf-exam-title">امتحان الفصل """ + ("الأول" if exam_num==1 else "الثاني" if exam_num==2 else "الأخير") + """</div>
        <div class="kashf-doc-title">كشف الدرجات</div>
      </div>
    """

    # ── معلومات الطالب ──
    html += f"""
      <div class="info-grid">
        <div class="info-cell">
          <span class="info-label">الاسم الكامل:</span>
          <span class="info-value">{s.get('الاسم','—')}</span>
        </div>
        <div class="info-cell">
          <span class="info-label">رقم النداء:</span>
          <span class="info-value">{s.get('الرقم', s.get('رقم النداء','—'))}</span>
        </div>
      </div>
    """

    # ── جدول الدرجات ──
    # أعمدة معدلات الامتحانات الثلاثة (rowspan على كل الصفوف)
    avg1 = fmt(s.get('معدل الامتحان الأول', s.get('معدل الامتحان الاول','')))
    avg2 = fmt(s.get('معدل الامتحان الثاني',''))
    avg3 = fmt(s.get('معدل الامتحان الأخير', s.get('معدل الامتحان الثالث','')))

    suffix = f" {exam_num}" if exam_num else ""

    html += """
      <table class="grades-table">
        <thead>
          <tr>
            <th>المواد</th>
            <th>الدرجات</th>
            <th>معدل الامتحان الأول</th>
            <th>معدل الامتحان الثاني</th>
            <th>معدل الامتحان الأخير</th>
          </tr>
        </thead>
        <tbody>
    """

    row_count = len(subjects)
    for i, (label, key, max_score) in enumerate(subjects):
        col_key = f"{label}{suffix}"
        score   = s.get(col_key, s.get(label, ''))
        score_display = f"{fmt(score, 2)}\\{max_score}" if max_score and score != '' else ''

        dark = ' dark-cell' if max_score is None else ''

        avg_cols = ""
        if i == 0:
            avg_cols = f"""
              <td rowspan="{row_count}" style="vertical-align:middle; font-size:18px; font-weight:bold; color:#1a7a1a;">
                {avg1}\\20
              </td>
              <td rowspan="{row_count}" style="vertical-align:middle; font-size:18px; font-weight:bold; color:#c0392b;">
                {avg2}\\20
              </td>
              <td rowspan="{row_count}" style="vertical-align:middle; font-size:18px; font-weight:bold; color:#1a7a1a;">
                {avg3}\\20
              </td>
            """

        html += f"""
          <tr>
            <td class="subject-name">{label}</td>
            <td class="{dark.strip()}">{score_display}</td>
            {avg_cols}
          </tr>
        """

    html += "</tbody></table>"

    # ── سطر الملخص ──
    total_key   = f"المجموع{suffix}"
    avg_key     = f"معدل الامتحان {'الأول' if exam_num==1 else 'الثاني' if exam_num==2 else 'الأخير'}"
    rank_key    = f"الرتبة{suffix}" if exam_num else "الرتبة العامة"
    verdict_key = f"القرار{suffix}" if exam_num else "القرار العام"

    total   = fmt(s.get(total_key, ''), 2)
    avg_val = fmt(s.get(avg_key, ''), 2)
    rank    = s.get(rank_key, s.get('الرتبة','—'))
    verdict = str(s.get(verdict_key, s.get('القرار',''))).strip()

    general_avg = fmt(s.get('المعدل العام',''), 2) if show_general else None

    passed = is_pass(s.get(avg_key, s.get('المعدل العام',0)))
    verdict_class  = "verdict-pass" if passed else "verdict-fail"
    verdict_symbol = "ناجح" if passed else "راسب"
    if verdict:
        verdict_symbol = verdict

    html += '<div class="summary-row">'
    html += f'<div class="sum-box"><div class="sum-label">المجموع</div><div class="sum-val">{total}\\200</div></div>'
    html += f'<div class="sum-box"><div class="sum-label">المعدل</div><div class="sum-avg">{avg_val}\\20</div></div>'

    if show_general and general_avg:
        html += f'<div class="sum-box"><div class="sum-label">المعدل العام</div><div class="sum-avg">{general_avg}\\20</div></div>'

    html += f'<div class="sum-box"><div class="sum-label">الرتبة</div><div class="sum-val">{rank}</div></div>'
    html += f'<div class="sum-box"><div class="sum-label">&nbsp;</div><div class="{verdict_class}">{verdict_symbol}</div></div>'
    html += '</div>'

    # ── توقيعات ──
    html += """
      <div class="sig-row">
        <div>المعلم: _______________</div>
        <div>المدير: _______________</div>
      </div>
    </div>
    """
    return html, passed

# ─────────────────────────────────────────────
# واجهة التطبيق
# ─────────────────────────────────────────────

st.markdown("""
<div style="text-align:center; padding: 20px 0 10px; direction:rtl;">
  <div style="font-size:40px;">🎓</div>
  <h1 style="color:#1a3c5e; font-family:'Amiri',serif; margin:4px 0;">بوابة نتائج التلاميذ</h1>
  <p style="color:#555; font-size:15px;">استعلم عن نتيجتك باستخدام الاسم أو رقم النداء</p>
</div>
""", unsafe_allow_html=True)

if not os.path.exists(EXCEL_FILE):
    st.error("⚠️ ملف النتائج (results.xlsx) غير موجود في مجلد التطبيق.")
    st.info("📌 ضع ملف `results.xlsx` في نفس مجلد `app.py` ثم أعد تشغيل التطبيق.")
    st.stop()

try:
    df = pd.read_excel(EXCEL_FILE)
except Exception as e:
    st.error(f"خطأ في قراءة الملف: {e}")
    st.stop()

# ── خانة البحث ──
col1, col2 = st.columns([3, 1])
with col1:
    query = st.text_input(
        "ابحث عن الطالب:",
        placeholder="أدخل رقم النداء أو الاسم الكامل...",
        label_visibility="collapsed"
    )
with col2:
    search = st.button("🔍 استعلام")

if search or query:
    if not query.strip():
        st.info("يرجى كتابة الاسم أو رقم النداء أولاً.")
        st.stop()

    q = str(query).strip()
    name_col   = 'الاسم'   if 'الاسم'   in df.columns else df.columns[1]
    number_col = 'الرقم'   if 'الرقم'   in df.columns else (
                 'رقم النداء' if 'رقم النداء' in df.columns else df.columns[0])

    match = df[
        (df[number_col].astype(str).str.strip() == q) |
        (df[name_col].astype(str).str.strip().str.contains(q, case=False, na=False))
    ]

    if match.empty:
        st.error(f"❌ لم يُعثر على نتيجة لـ «{query}». تحقق من الاسم أو الرقم.")
        st.stop()

    s = match.iloc[0].to_dict()
    st.success(f"✅ تم العثور على: **{s.get(name_col,'—')}**")
    st.divider()

    tab1, tab2, tab3 = st.tabs(["📝 الامتحان الأول", "📝 الامتحان الثاني", "🏆 الامتحان الأخير"])

    with tab1:
        html1, _ = build_kashf(s, 1, SUBJECTS)
        st.markdown(html1, unsafe_allow_html=True)

    with tab2:
        html2, _ = build_kashf(s, 2, SUBJECTS)
        st.markdown(html2, unsafe_allow_html=True)

    with tab3:
        html3, passed = build_kashf(s, 3, SUBJECTS, show_general=True)
        st.markdown(html3, unsafe_allow_html=True)

        # ── رسالة النتيجة النهائية ──
        verdict_general = str(s.get('القرار العام', s.get('القرار3', ''))).strip()
        final_passed    = is_pass(s.get('المعدل العام', s.get('معدل الامتحان الأخير', 0)))

        if "ناجح" in verdict_general or "منتقل" in verdict_general or (not verdict_general and final_passed):
            label = verdict_general or "ناجح 🎈"
            st.markdown(f'<div class="success-box">🏆 النتيجة النهائية للعام الدراسي: {label}</div>',
                        unsafe_allow_html=True)
            st.balloons()
        elif "راسب" in verdict_general or "مكرر" in verdict_general or (not verdict_general and not final_passed):
            label = verdict_general or "راسب"
            st.markdown(f'<div class="fail-box">😔 النتيجة النهائية للعام الدراسي: {label}</div>',
                        unsafe_allow_html=True)
