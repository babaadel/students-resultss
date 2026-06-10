import streamlit as st
import pandas as pd
import os

# 1. إعدادات الصفحة وجعل التخطيط متجاوباً تلقائياً
st.set_page_config(page_title="منصة نتائج التلاميذ", page_icon="🎓", layout="centered")

# 2. تصميم CSS محسن بالكامل
st.markdown("""
    <style>
    .stApp { direction: rtl; text-align: right; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    
    /* تنسيق زر الاستعلام الأساسي */
    div.stButton > button { width: 100%; border-radius: 12px; background-color: #2563eb; color: white; height: 3.2em; font-weight: bold; font-size: 16px; border: none; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); }
    div.stButton > button:hover { background-color: #1d4ed8; }
    
    /* تنسيق علامات التبويب والخانات */
    button[data-baseweb="tab"] { font-size: 16px !important; font-weight: bold !important; padding: 12px 20px !important; }
    
    /* تنسيق رسائل النجاح والرسوب */
    .success-box { color: #15803d; background-color: #f0fdf4; border: 1px solid #bbf7d0; padding: 18px; border-radius: 14px; text-align: center; font-size: 18px; font-weight: bold; margin: 15px 0; }
    .fail-box { color: #b91c1c; background-color: #fef2f2; border: 1px solid #fecaca; padding: 18px; border-radius: 14px; text-align: center; font-size: 18px; font-weight: bold; margin: 15px 0; }
    
    /* تحسين جداول البيانات */
    .stTable { width: 100% !important; border-radius: 10px; overflow: hidden; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎓 بوابة نتائج التلاميذ")
st.write("استخدم الاسم أو الرقم للاستعلام عن النتيجة")

# ===== دالة توليد HTML لشكلية الكشف الرسمي =====
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

    if "ناجح" in decision_val or "منتقل" in decision_val:
        dec_color = "#16a34a"
    else:
        dec_color = "#dc2626"

    html = f"""<!DOCTYPE html>
<html dir="rtl" lang="ar">
<head>
<meta charset="UTF-8">
<title>كشف درجات - {s.get('الاسم','')}</title>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: 'Segoe UI', Tahoma, sans-serif; direction: rtl; background: white; color: #111; padding: 20px; }}
  .outer-border {{ border: 3px solid #000; padding: 10px; max-width: 780px; margin: auto; }}
  .top-header {{ display: flex; justify-content: space-between; align-items: flex-start; border-bottom: 2px solid #000; padding-bottom: 10px; margin-bottom: 10px; }}
  .top-header .col {{ font-size: 13px; line-height: 1.9; }}
  .top-header .col-center {{ text-align: center; }}
  .top-header strong {{ font-size: 14px; }}
  .motto {{ font-size: 12px; color: #555; text-align: left; margin-bottom: 4px; }}
  .exam-title {{ text-align: center; font-size: 22px; font-weight: bold; margin: 10px 0 4px 0; border-bottom: 1px solid #ccc; padding-bottom: 6px; }}
  .kashf-title {{ text-align: center; background: #d4edda; border: 1px solid #aaa; border-radius: 6px; font-size: 20px; font-weight: bold; padding: 6px 20px; margin: 8px auto; width: fit-content; }}
  .student-info {{ display: flex; justify-content: space-between; font-size: 13px; margin: 10px 0; padding: 0 4px; }}
  .student-info span {{ font-weight: bold; color: #1a56db; }}
  table {{ width: 100%; border-collapse: collapse; margin-top: 6px; font-size: 13px; }}
  th {{ background: #f0f0f0; border: 1px solid #333; padding: 7px 10px; text-align: center; }}
  td {{ border: 1px solid #333; padding: 6px 10px; }}
  .avg-cell {{ text-align: center; font-weight: bold; color: #c00; font-size: 15px; }}
  .decision-cell {{ text-align: center; font-weight: bold; font-size: 20px; color: {dec_color}; }}
  .footer-row {{ display: flex; justify-content: space-between; margin-top: 20px; font-size: 14px; font-weight: bold; border-top: 1px solid #aaa; padding-top: 10px; }}
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
    <div class="col col-center"><div style="font-size:48px;">🇲🇷</div></div>
    <div class="col" style="text-align:left;">
      <div class="motto">شـرف – إخـاء – عـدل</div>
      <strong>العام الدراسي: 2025\\2026</strong><br>
      المـــدرسة: كنكوصة 4<br>
      القسـم: الثالث ابتدائي
    </div>
  </div>

  <div class="exam-title">{exam_title}</div>
  <div class="kashf-title">كشف الدرجات</div>

  <div class="student-info">
    <div>الاسم الكامل: <span>{s.get('الاسم','')}</span></div>
    <div>الرقم المدرسي: <span>{s.get('الرقم','')}</span></div>
    <div>رقم النداء: <span>{s.get('الرقم','')}</span></div>
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
        <td>اللغة العربية</td>
        <td style="text-align:center;">{format_value(s.get(f'اللغة العربية {suffix}'))}</td>
        <td rowspan="3" class="avg-cell">{avg1}\\20</td>
      </tr>
      <tr>
        <td>التربية الإسلامية</td>
        <td style="text-align:center;">{format_value(s.get(f'التربية الاسلامية {suffix}'))}</td>
      </tr>
      <tr>
        <td>الرياضيات</td>
        <td style="text-align:center;">{format_value(s.get(f'الرياضيات {suffix}'))}</td>
      </tr>
      <tr>
        <td>الفرنسية</td>
        <td style="text-align:center;">{format_value(s.get(f'الفرنسية {suffix}'))}</td>
        <th style="background:#f0f0f0;">الملاحظات</th>
      </tr>
      <tr>
        <td>العلوم الطبيعية</td>
        <td style="text-align:center;">{format_value(s.get(f'العلوم الطبيعية {suffix}'))}</td>
        <td rowspan="3" class="avg-cell">{avg2}\\20</td>
      </tr>
      <tr>
        <td>التاريخ والجغرافيا</td>
        <td style="text-align:center;">{format_value(s.get(f'التاريخ والجغرافيا {suffix}'))}</td>
      </tr>
      <tr>
        <td>التربية المدنية</td>
        <td style="text-align:center;">{format_value(s.get(f'التربية المدنية {suffix}'))}</td>
      </tr>
      <tr>
        <td>التربية الفنية</td>
        <td style="text-align:center;">{format_value(s.get(f'التربية الفنية {suffix}'))}</td>
        <th style="background:#f0f0f0;">معدل الامتحان الحالي</th>
      </tr>
      <tr>
        <td>الرياضة البدنية</td>
        <td style="text-align:center;">{format_value(s.get(f'الرياضة البدنية {suffix}'))}</td>
        <td rowspan="4" class="avg-cell">{avg3}\\20</td>
      </tr>
      <tr>
        <td>المجموع</td>
        <td style="text-align:center;">{total_val}\\200</td>
      </tr>
      <tr>
        <td style="font-weight:bold;">المعدل بالفصل</td>
        <td style="text-align:center;font-weight:bold;color:#c00;">{exam_avg}\\20</td>
      </tr>
      <tr>
        <td colspan="2" style="text-align:center;">المعدل العام: <strong style="color:#16a34a;">{avg_general}</strong></td>
      </tr>
      <tr>
        <td colspan="2" style="text-align:center;">الرتبة: <strong>{rank_val}</strong></td>
        <td class="decision-cell">{decision_val}</td>
      </tr>
    </tbody>
  </table>

  <div class="footer-row">
    <div>المعلم: ________________</div>
    <div>المدير: ________________</div>
  </div>
</div>
