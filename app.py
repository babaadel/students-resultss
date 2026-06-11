import streamlit as st
import pandas as pd
import os
import base64

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة نتائج التلاميذ", page_icon="🎓", layout="centered")

# دالة لتحويل الصورة المحلية إلى Base64
def get_image_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as image_file:
            ext = path.split('.')[-1].lower()
            mime = "image/png" if ext == "png" else "image/jpeg"
            return f"data:{mime};base64," + base64.b64encode(image_file.read()).decode()
    return ""

LOGO_FILE = "logo.png"
logo_base64 = get_image_base64(LOGO_FILE)

# 2. تصميم CSS الكامل للموقع
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Amiri:wght@400;700&family=Cairo:wght@400;600;700;900&display=swap');

    /* ===== خلفية الموقع بلون العلم الموريتاني ===== */
    .stApp {{
        direction: rtl;
        text-align: right;
        font-family: 'Cairo', 'Segoe UI', sans-serif;
        background: linear-gradient(160deg, #006233 0%, #006233 40%, #cd2a3e 100%) !important;
        min-height: 100vh;
    }}

    /* ===== رأسية الموقع الرئيسية ===== */
    .site-header {{
        background: linear-gradient(135deg, #006233 0%, #004d27 40%, #8b0000 80%, #cd2a3e 100%);
        border: 3px solid #ffd700;
        border-radius: 16px;
        padding: 20px 25px 15px 25px;
        margin-bottom: 28px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.4), inset 0 1px 0 rgba(255,215,0,0.3);
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 15px;
    }}
    .site-header .header-right {{
        text-align: right;
        color: white;
        font-size: 13px;
        line-height: 2;
        flex: 1;
    }}
    .site-header .header-right .main-title {{
        font-size: 15px;
        font-weight: 700;
        color: #ffd700;
        letter-spacing: 0.5px;
    }}
    .site-header .header-right .sub-title {{
        font-size: 12.5px;
        font-weight: 400;
        color: #e0e0e0;
    }}
    .site-header .header-center {{
        text-align: center;
        flex: 0 0 auto;
    }}
    .site-header .header-center img {{
        width: 100px;
        height: 100px;
        object-fit: contain;
        filter: drop-shadow(0 3px 8px rgba(0,0,0,0.5));
        border-radius: 50%;
        border: 2px solid #ffd700;
        background: white;
        padding: 3px;
    }}
    .site-header .header-left {{
        text-align: left;
        color: white;
        font-size: 13px;
        line-height: 2;
        flex: 1;
    }}
    .site-header .header-left .motto {{
        font-size: 13px;
        font-weight: 700;
        color: #ffd700;
        margin-bottom: 4px;
    }}
    .site-header .header-left .sub-title {{
        font-size: 12.5px;
        font-weight: 400;
        color: #e0e0e0;
    }}

    /* ===== عنوان البوابة الرئيسي ===== */
    .portal-title-container {{
        text-align: center;
        margin: 10px 0 25px 0;
        padding: 20px 15px;
        background: rgba(255,255,255,0.08);
        border-radius: 14px;
        border: 1px solid rgba(255,215,0,0.3);
        backdrop-filter: blur(4px);
    }}
    .portal-title-icon {{
        font-size: 52px;
        display: block;
        margin-bottom: 8px;
        text-shadow: 0 4px 12px rgba(0,0,0,0.3);
    }}
    .portal-title-text {{
        font-family: 'Amiri', serif;
        font-size: 32px;
        font-weight: 700;
        color: #ffd700;
        text-shadow: 0 3px 10px rgba(0,0,0,0.5), 0 0 20px rgba(255,215,0,0.3);
        letter-spacing: 1px;
        margin-bottom: 6px;
    }}
    .portal-title-sub {{
        font-size: 14px;
        color: rgba(255,255,255,0.8);
        font-weight: 400;
    }}
    .portal-divider {{
        width: 120px;
        height: 3px;
        background: linear-gradient(90deg, transparent, #ffd700, transparent);
        margin: 10px auto 0 auto;
        border-radius: 2px;
    }}

    /* ===== صندوق البحث ===== */
    .search-container {{
        background: rgba(255,255,255,0.95);
        border-radius: 16px;
        padding: 28px 24px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        margin-bottom: 20px;
        border: 1px solid rgba(255,215,0,0.4);
    }}

    /* ===== تنسيق حقل الإدخال ===== */
    .stTextInput > div > div > input {{
        border-radius: 10px !important;
        border: 2px solid #006233 !important;
        padding: 12px 16px !important;
        font-size: 15px !important;
        font-family: 'Cairo', sans-serif !important;
        text-align: right !important;
        direction: rtl !important;
    }}
    .stTextInput > div > div > input:focus {{
        border-color: #ffd700 !important;
        box-shadow: 0 0 0 3px rgba(255,215,0,0.2) !important;
    }}

    /* ===== زر الاستعلام المتوسط الموسع ===== */
    div.stButton {{
        display: flex;
        justify-content: center;
        margin-top: 12px;
    }}
    div.stButton > button {{
        width: 65% !important;
        border-radius: 12px !important;
        background: linear-gradient(135deg, #006233, #004d27) !important;
        color: white !important;
        height: 3.2em !important;
        font-weight: 700 !important;
        font-size: 16px !important;
        border: 2px solid #ffd700 !important;
        box-shadow: 0 4px 15px rgba(0,98,51,0.4) !important;
        font-family: 'Cairo', sans-serif !important;
        letter-spacing: 0.5px;
        transition: all 0.3s ease !important;
    }}
    div.stButton > button:hover {{
        background: linear-gradient(135deg, #004d27, #003319) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(0,98,51,0.5) !important;
    }}

    /* ===== رسائل النجاح والرسوب ===== */
    .success-box {{
        color: #fff;
        background: linear-gradient(135deg, #15803d, #166534);
        border: 2px solid #4ade80;
        padding: 20px;
        border-radius: 14px;
        text-align: center;
        font-size: 20px;
        font-weight: bold;
        margin: 15px 0;
        box-shadow: 0 4px 15px rgba(21,128,61,0.4);
        font-family: 'Cairo', sans-serif;
    }}
    .fail-box {{
        color: #fff;
        background: linear-gradient(135deg, #b91c1c, #991b1b);
        border: 2px solid #f87171;
        padding: 20px;
        border-radius: 14px;
        text-align: center;
        font-size: 20px;
        font-weight: bold;
        margin: 15px 0;
        box-shadow: 0 4px 15px rgba(185,28,28,0.4);
        font-family: 'Cairo', sans-serif;
    }}

    /* ===== بطاقة النتيجة ===== */
    .result-card {{
        background: rgba(255,255,255,0.97);
        border-radius: 16px;
        padding: 20px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        border: 1px solid rgba(255,215,0,0.3);
    }}

    /* ===== تنسيق علامات التبويب ===== */
    button[data-baseweb="tab"] {{
        font-size: 14px !important;
        font-weight: 700 !important;
        font-family: 'Cairo', sans-serif !important;
    }}

    /* ===== إخفاء عناصر Streamlit الافتراضية ===== */
    #MainMenu {{ visibility: hidden; }}
    footer {{ visibility: hidden; }}
    header {{ visibility: hidden; }}
    .block-container {{ padding-top: 1.5rem !important; padding-bottom: 2rem !important; }}
    </style>

    <!-- رأسية الموقع -->
    <div class="site-header">
        <div class="header-right">
            <div class="main-title">الجمهورية الإسلامية الموريتانية</div>
            <div class="sub-title">وزارة التربية وإصلاح النظام التعليمي</div>
            <div class="sub-title">الإدارة الجهوية بولاية لعصابه</div>
            <div class="sub-title">مفتشية التعليم بمقاطعة كنكوصة</div>
        </div>
        <div class="header-center">
            <img src="{logo_base64 if logo_base64 else 'https://upload.wikimedia.org/wikipedia/commons/4/43/Emblem_of_Mauritania.svg'}" alt="الشعار الرسمي">
        </div>
        <div class="header-left">
            <div class="motto">شـرف – إخـاء – عـدل</div>
            <div class="sub-title">العام الدراسي: 2025/2026</div>
            <div class="sub-title">المدرسة: كنكوصة 4</div>
            <div class="sub-title">القسم: الثالث ابتدائي</div>
        </div>
    </div>

    <!-- عنوان البوابة -->
    <div class="portal-title-container">
        <span class="portal-title-icon">🎓</span>
        <div class="portal-title-text">بوابة نتائج التلاميذ</div>
        <div class="portal-title-sub">استعلم عن نتيجتك باستخدام الاسم أو الرقم المدرسي</div>
        <div class="portal-divider"></div>
    </div>
    """, unsafe_allow_html=True)


# ===== دالة توليد HTML لكشف الدرجات الرسمي المزخرف =====
def build_report_html(s, format_value, exam_num, logo_b64):
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
        dec_color = "#15803d"
        dec_bg = "#f0fdf4"
        dec_border = "#86efac"
    else:
        dec_color = "#b91c1c"
        dec_bg = "#fef2f2"
        dec_border = "#fca5a5"

    html_template = """<!DOCTYPE html>
<html dir="rtl" lang="ar">
<head>
<meta charset="UTF-8">
<title>كشف درجات</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Amiri:wght@400;700&family=Cairo:wght@400;600;700;900&display=swap');
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    font-family: 'Cairo', 'Segoe UI', Tahoma, sans-serif;
    direction: rtl;
    background: #f5f5f5;
    color: #111;
    padding: 20px;
    print-color-adjust: exact;
    -webkit-print-color-adjust: exact;
  }

  /* ===== الإطار الخارجي المزخرف ===== */
  .outer-frame {
    max-width: 800px;
    margin: auto;
    background: white;
    border: 4px double #006233;
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 8px 32px rgba(0,0,0,0.15);
    position: relative;
  }
  /* زخرفة الزوايا */
  .outer-frame::before {
    content: '';
    position: absolute;
    inset: 8px;
    border: 1px solid rgba(0,98,51,0.2);
    border-radius: 8px;
    pointer-events: none;
    z-index: 0;
  }

  /* ===== الرأسية ===== */
  .top-header {
    background: linear-gradient(135deg, #006233 0%, #004d27 45%, #8b0000 75%, #cd2a3e 100%);
    padding: 18px 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 3px solid #ffd700;
    gap: 10px;
    position: relative;
    z-index: 1;
  }
  .top-header .col { color: white; font-size: 12.5px; line-height: 2; }
  .top-header .col-right { text-align: right; }
  .top-header .col-left { text-align: left; }
  .top-header .col-center { text-align: center; }
  .top-header .col-center img {
    width: 90px; height: 90px;
    object-fit: contain;
    border-radius: 50%;
    border: 2px solid #ffd700;
    background: white;
    padding: 3px;
    filter: drop-shadow(0 3px 8px rgba(0,0,0,0.4));
  }
  .top-header strong { color: #ffd700; font-size: 13.5px; font-weight: 700; }
  .top-header .motto { color: #ffd700; font-weight: 700; font-size: 13px; margin-bottom: 4px; }

  /* ===== شريط العنوان ===== */
  .titles-section {
    background: linear-gradient(180deg, #f8f9fa 0%, #ffffff 100%);
    border-bottom: 2px solid #e5e7eb;
    padding: 18px 20px 14px;
    text-align: center;
    position: relative;
    z-index: 1;
  }
  .exam-title {
    font-family: 'Amiri', serif;
    font-size: 22px;
    font-weight: 700;
    color: #1a1a2e;
    letter-spacing: 0.5px;
    margin-bottom: 8px;
  }
  .kashf-title-wrapper {
    display: inline-block;
    background: linear-gradient(135deg, #006233, #004d27);
    border-radius: 30px;
    padding: 6px 40px;
    border: 2px solid #ffd700;
    box-shadow: 0 3px 10px rgba(0,98,51,0.3);
  }
  .kashf-title {
    font-family: 'Amiri', serif;
    font-size: 20px;
    font-weight: 700;
    color: #ffd700;
    letter-spacing: 1px;
  }
  .ornament-line {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
    margin-top: 12px;
    color: #006233;
    font-size: 16px;
  }
  .ornament-line::before, .ornament-line::after {
    content: '';
    width: 80px;
    height: 2px;
    background: linear-gradient(90deg, transparent, #006233);
  }
  .ornament-line::after { background: linear-gradient(90deg, #006233, transparent); }

  /* ===== بيانات التلميذ ===== */
  .student-info {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: linear-gradient(135deg, #eff6ff, #f0fdf4);
    border: 1px solid #bfdbfe;
    border-radius: 10px;
    padding: 12px 18px;
    margin: 16px 16px 12px;
    font-size: 13px;
    position: relative;
    z-index: 1;
  }
  .student-info .info-item { display: flex; gap: 6px; align-items: center; }
  .student-info .info-label { color: #4b5563; font-weight: 500; }
  .student-info .info-value { color: #1d4ed8; font-weight: 700; font-size: 14px; }

  /* ===== الجدول الرئيسي ===== */
  .table-wrapper { padding: 0 16px 16px; position: relative; z-index: 1; }
  table { width: 100%; border-collapse: collapse; font-size: 13px; }
  th {
    background: linear-gradient(180deg, #006233 0%, #004d27 100%);
    color: #ffd700;
    border: 1px solid #004d27;
    padding: 10px 12px;
    text-align: center;
    font-weight: 700;
    font-size: 13.5px;
    letter-spacing: 0.3px;
  }
  td {
    border: 1px solid #d1d5db;
    padding: 8px 12px;
    font-size: 13px;
  }
  tr:nth-child(even) td { background: #fafafa; }
  tr:hover td { background: #f0fdf4; }

  /* خلايا خاصة */
  .subject-cell { font-weight: 600; color: #1f2937; }
  .score-cell { text-align: center; font-weight: 600; color: #1e40af; }
  .avg-cell {
    text-align: center;
    font-weight: 700;
    color: #b91c1c;
    font-size: 15px;
    background: linear-gradient(180deg, #fff7ed, #fff) !important;
    vertical-align: middle;
  }
  .remarks-header {
    background: linear-gradient(180deg, #fef9c3, #fefce8) !important;
    color: #78350f !important;
    font-weight: 700 !important;
    text-align: center;
    border: 1px solid #d1d5db !important;
    padding: 8px 12px;
  }

  /* صف المجموع */
  .total-row td { background: linear-gradient(135deg, #f0fdf4, #fff) !important; font-weight: 700; }
  .total-label { font-weight: 700; color: #1f2937; }
  .total-value { text-align: center; font-weight: 700; color: #166534; font-size: 14px; }

  /* صف المعدل العام */
  .general-avg-row td {
    background: linear-gradient(135deg, #eff6ff, #fff) !important;
    text-align: center;
    font-size: 14px;
    font-weight: 600;
    color: #374151;
  }
  .general-avg-value { color: #15803d; font-size: 17px; font-weight: 700; }

  /* صف الرتبة والقرار */
  .rank-row td { background: #f8fafc !important; }
  .rank-cell { text-align: center; font-size: 14px; font-weight: 600; }
  .rank-value { color: #1d4ed8; font-size: 16px; font-weight: 700; }
  .decision-cell {
    text-align: center;
    font-size: 18px;
    font-weight: 700;
    padding: 12px !important;
    background: __DEC_BG__ !important;
    color: __DEC_COLOR__;
    border: 2px solid __DEC_BORDER__ !important;
    border-radius: 6px;
  }

  /* ===== التذييل ===== */
  .footer-section {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 15px 20px;
    background: linear-gradient(180deg, #f9fafb, #f3f4f6);
    border-top: 2px dashed #d1d5db;
    font-size: 13px;
    font-weight: 600;
    color: #374151;
    position: relative;
    z-index: 1;
  }
  .footer-section .sign-line {
    border-bottom: 1px solid #6b7280;
    min-width: 130px;
    display: inline-block;
    margin-right: 5px;
  }

  /* ===== زخرفة هامشية ===== */
  .side-ornament {
    writing-mode: vertical-rl;
    text-orientation: mixed;
    position: absolute;
    right: 8px;
    top: 50%;
    transform: translateY(-50%);
    font-size: 11px;
    color: rgba(0,98,51,0.15);
    font-family: 'Amiri', serif;
    letter-spacing: 3px;
    z-index: 0;
    user-select: none;
  }

  @media print {
    body { padding: 0; background: white; }
    .outer-frame { box-shadow: none; }
  }
</style>
</head>
<body>
<div class="outer-frame">
  <div class="side-ornament">بسم الله الرحمن الرحيم</div>

  <!-- الرأسية -->
  <div class="top-header">
    <div class="col col-right">
      <strong>الجمهورية الإسلامية الموريتانية</strong><br>
      وزارة التربية وإصلاح النظام التعليمي<br>
      الإدارة الجهوية بولاية لعصابه<br>
      مفتشية التعليم بمقاطعة كنكوصة
    </div>
    <div class="col col-center">
      <img src="__LOGO_URL__" alt="الشعار الرسمي">
    </div>
    <div class="col col-left">
      <div class="motto">شـرف – إخـاء – عـدل</div>
      العام الدراسي: 2025/2026<br>
      المدرسة: كنكوصة 4<br>
      القسم: الثالث ابتدائي
    </div>
  </div>

  <!-- العنوان -->
  <div class="titles-section">
    <div class="exam-title">__EXAM_TITLE__</div>
    <div class="kashf-title-wrapper">
      <span class="kashf-title">كـشـف الـدرجـات</span>
    </div>
    <div class="ornament-line">✦</div>
  </div>

  <!-- بيانات التلميذ -->
  <div class="student-info">
    <div class="info-item">
      <span class="info-label">الاسم الكامل:</span>
      <span class="info-value">__STUDENT_NAME__</span>
    </div>
    <div class="info-item">
      <span class="info-label">الرقم المدرسي:</span>
      <span class="info-value">__STUDENT_ID__</span>
    </div>
    <div class="info-item">
      <span class="info-label">رقم النداء:</span>
      <span class="info-value">__STUDENT_ID__</span>
    </div>
  </div>

  <!-- الجدول -->
  <div class="table-wrapper">
    <table>
      <thead>
        <tr>
          <th style="width:34%;">المواد</th>
          <th style="width:22%;">الدرجات</th>
          <th style="width:22%;">معدلات الفصول</th>
          <th style="width:22%;">الملاحظات</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td class="subject-cell">اللغة العربية</td>
          <td class="score-cell">__ARABIC__</td>
          <td rowspan="3" class="avg-cell">__AVG1__ / 20</td>
          <td rowspan="3"></td>
        </tr>
        <tr>
          <td class="subject-cell">التربية الإسلامية</td>
          <td class="score-cell">__ISLAMIC__</td>
        </tr>
        <tr>
          <td class="subject-cell">الرياضيات</td>
          <td class="score-cell">__MATH__</td>
        </tr>
        <tr>
          <td class="subject-cell">الفرنسية</td>
          <td class="score-cell">__FRENCH__</td>
          <td class="avg-cell">__AVG2__ / 20</td>
          <td class="remarks-header">الملاحظات</td>
        </tr>
        <tr>
          <td class="subject-cell">العلوم الطبيعية</td>
          <td class="score-cell">__SCIENCE__</td>
          <td rowspan="3" class="avg-cell">__AVG3__ / 20</td>
          <td rowspan="3"></td>
        </tr>
        <tr>
          <td class="subject-cell">التاريخ والجغرافيا</td>
          <td class="score-cell">__HISTORY__</td>
        </tr>
        <tr>
          <td class="subject-cell">التربية المدنية</td>
          <td class="score-cell">__CIVICS__</td>
        </tr>
        <tr>
          <td class="subject-cell">التربية الفنية</td>
          <td class="score-cell">__ART__</td>
          <td colspan="2" style="text-align:center; font-size:12.5px; color:#4b5563; background:#fffdf0;">
            معدل الامتحان الحالي
          </td>
        </tr>
        <tr>
          <td class="subject-cell">الرياضة البدنية</td>
          <td class="score-cell">__SPORT__</td>
          <td rowspan="3" class="avg-cell" style="font-size:17px;">__EXAM_AVG__ / 20</td>
          <td rowspan="3"></td>
        </tr>
        <tr class="total-row">
          <td class="total-label">المجموع</td>
          <td class="total-value">__TOTAL__ / 200</td>
        </tr>
        <tr>
          <td style="font-weight:700; color:#b91c1c; background:#fff1f2;">المعدل بالفصل</td>
          <td style="text-align:center; font-weight:700; color:#b91c1c; background:#fff1f2; font-size:14px;">__EXAM_AVG__ / 20</td>
        </tr>
        <tr>
          <td colspan="3" class="general-avg-row" style="border:1px solid #d1d5db; padding:10px; text-align:center; font-size:14px; font-weight:600; color:#374151; background:linear-gradient(135deg,#eff6ff,#fff);">
            المعدل العام: <span class="general-avg-value">__AVG_GENERAL__</span>
          </td>
          <td></td>
        </tr>
        <tr class="rank-row">
          <td colspan="2" class="rank-cell" style="border:1px solid #d1d5db; padding:10px;">
            الرتبة: <span class="rank-value">__RANK__</span>
          </td>
          <td colspan="2" class="decision-cell">__DECISION__</td>
        </tr>
      </tbody>
    </table>
  </div>

  <!-- التذييل -->
  <div class="footer-section">
    <div>المعلم: <span class="sign-line">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span></div>
    <div>المدير: <span class="sign-line">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span></div>
  </div>
</div>
<script>window.print();</script>
</body>
</html>"""

    html = html_template.replace("__LOGO_URL__", logo_b64)
    html = html.replace("__DEC_COLOR__", dec_color)
    html = html.replace("__DEC_BG__", dec_bg)
    html = html.replace("__DEC_BORDER__", dec_border)
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


# دالة تقريب الأرقام
def format_value(val):
    try:
        return round(float(val), 2)
    except (ValueError, TypeError):
        return val if pd.notna(val) else 'غير متوفر'


# ===== الجزء الرئيسي =====
EXCEL_FILE = 'results.xlsx'

if not os.path.exists(EXCEL_FILE):
    st.error("⚠️ ملف النتائج (results.xlsx) غير موجود. يرجى رفعه في GitHub.")
else:
    try:
        df = pd.read_excel(EXCEL_FILE)

        if "student_data" not in st.session_state:
            st.session_state.student_data = None
        if "searched" not in st.session_state:
            st.session_state.searched = False

        # صندوق البحث
        st.markdown('<div class="search-container">', unsafe_allow_html=True)
        query = st.text_input(
            "🔍 أدخل رقم التلميذ أو الاسم الكامل:",
            placeholder="مثال: 10 أو أحمد محمد"
        )
        if st.button("🔎 استعلام عن النتيجة"):
            if query:
                q = str(query).strip()
                match = df[
                    (df['الرقم'].astype(str).str.strip() == q) |
                    (df['الاسم'].str.strip().str.contains(q, case=False, na=False))
                ]
                if not match.empty:
                    st.session_state.student_data = match.iloc[0].to_dict()
                    st.session_state.searched = True
                else:
                    st.session_state.student_data = None
                    st.session_state.searched = True
                    st.error(f"❌ لم يتم العثور على نتيجة لـ '{query}'.")
            else:
                st.info("يرجى كتابة الاسم أو الرقم أولاً.")
        st.markdown('</div>', unsafe_allow_html=True)

        # عرض النتائج
        if st.session_state.searched and st.session_state.student_data:
            s = st.session_state.student_data

            st.markdown('<div class="result-card">', unsafe_allow_html=True)
            st.divider()
            st.header(f"مرحباً، {s.get('الاسم', 'أيها التلميذ')} 👋")
            st.info(f"رقم التلميذ: **{s.get('الرقم', 'غير متوفر')}**")

            subjects_list = [
                'اللغة العربية', 'التربية الاسلامية', 'الرياضيات', 'الفرنسية',
                'العلوم الطبيعية', 'التاريخ والجغرافيا', 'التربية الفنية',
                'التربية المدنية', 'الرياضة البدنية'
            ]

            tab1, tab2, tab3 = st.tabs(["📝 الامتحان الأول", "📝 الامتحان الثاني", "🏆 الامتحان الأخير"])

            # --- الامتحان الأول ---
            with tab1:
                st.subheader("📊 كشف درجات الامتحان الأول")
                labels1 = list(subjects_list)
                values1 = [format_value(s.get(f'{sub} 1')) for sub in subjects_list]
                labels1.extend(['المجموع', 'معدل الامتحان الأول', 'الرتبة', 'القرار'])
                values1.extend([
                    format_value(s.get('المجموع 1')),
                    format_value(s.get('معدل الامتحان الأول')),
                    s.get('الرتبة 1', 'غير متوفر'),
                    s.get('القرار 1', 'غير متوفر')
                ])
                st.table(pd.DataFrame({'المادة / البيان': labels1, 'النتيجة': values1}))
                report1_html = build_report_html(s, format_value, exam_num=1, logo_b64=logo_base64)
                st.download_button(
                    label="🖨️ تحميل كشف الامتحان الأول للطباعة",
                    data=report1_html,
                    file_name=f"كشف_الامتحان_الأول_{s.get('الاسم')}.html",
                    mime="text/html"
                )

            # --- الامتحان الثاني ---
            with tab2:
                st.subheader("📊 كشف درجات الامتحان الثاني")
                labels2 = list(subjects_list)
                values2 = [format_value(s.get(f'{sub} 2')) for sub in subjects_list]
                labels2.extend(['المجموع', 'معدل الامتحان الثاني', 'الرتبة', 'القرار'])
                values2.extend([
                    format_value(s.get('المجموع 2')),
                    format_value(s.get('معدل الامتحان الثاني')),
                    s.get('الرتبة 2', 'غير متوفر'),
                    s.get('القرار 2', 'غير متوفر')
                ])
                st.table(pd.DataFrame({'المادة / البيان': labels2, 'النتيجة': values2}))
                report2_html = build_report_html(s, format_value, exam_num=2, logo_b64=logo_base64)
                st.download_button(
                    label="🖨️ تحميل كشف الامتحان الثاني للطباعة",
                    data=report2_html,
                    file_name=f"كشف_الامتحان_الثاني_{s.get('الاسم')}.html",
                    mime="text/html"
                )

            # --- الامتحان الأخير ---
            with tab3:
                st.subheader("📊 كشف درجات الامتحان الأخير والنهائي")
                labels3 = list(subjects_list)
                values3 = [format_value(s.get(f'{sub} 3')) for sub in subjects_list]
                labels3.extend(['المجموع', 'معدل الامتحان الأول', 'معدل الامتحان الثاني',
                                 'معدل الامتحان الأخير', 'المعدل العام', 'الرتبة العامة', 'القرار العام'])
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
                report3_html = build_report_html(s, format_value, exam_num=3, logo_b64=logo_base64)
                st.download_button(
                    label="🖨️ تحميل كشف الامتحان النهائي للطباعة",
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

            st.markdown('</div>', unsafe_allow_html=True)

    except Exception as e:
        st.error(f"حدث خطأ في قراءة البيانات: {e}")
