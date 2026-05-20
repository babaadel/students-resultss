import streamlit as st
import pandas as pd
import os

# إعدادات الصفحة
st.set_page_config(page_title="منصة نتائج التلاميذ", page_icon="🎓", layout="centered")

# تصميم CSS مخصص - تم تصحيح الخاصية هنا
st.markdown("""
    <style>
    .stApp { direction: rtl; text-align: right; }
    .main { background-color: #f8fafc; }
    div.stButton > button { width: 100%; border-radius: 10px; background-color: #2563eb; color: white; height: 3em; font-weight: bold; }
    .success-text { color: #166534; background-color: #dcfce7; padding: 20px; border-radius: 15px; text-align: center; font-size: 20px; font-weight: bold; }
    .fail-text { color: #991b1b; background-color: #fee2e2; padding: 20px; border-radius: 15px; text-align: center; font-size: 20px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎓 بوابة نتائج التلاميذ")
st.write("أدخل اسمك الكامل أو رقمك الخاص للاستعلام عن النتيجة")

# اسم ملف المدير
EXCEL_FILE = 'results.xlsx'

if not os.path.exists(EXCEL_FILE):
    st.error("⚠️ ملف النتائج (results.xlsx) غير موجود. يرجى من المدير رفعه في GitHub.")
else:
    # تحميل البيانات
    df = pd.read_excel(EXCEL_FILE)
    
    # حقل البحث
    query = st.text_input("بحث (الرقم أو الاسم)", placeholder="أدخل بياناتك هنا...")
    
    if st.button("عرض النتيجة"):
        if query:
            # منطق البحث
            match = df[(df['الرقم'].astype(str).str.strip() == query.strip()) | 
                       (df['الاسم'].str.strip() == query.strip())]
            
            if not match.empty:
                s = match.iloc[0].to_dict()
                
                st.divider()
                st.header(f"مرحباً، {s['الاسم']} 👋")
                
                # عرض المعدل والرتبة في أعمدة
                col1, col2 = st.columns(2)
                col1.metric("المعدل العام", s['المعدل'])
                col2.metric("الرتبة", s['الرتبة'])
                
                # القرار والاحتفال
                if "ناجح" in str(s['القرار']):
                    st.markdown(f'<div class="success-text">🎉 ألف مبروك النجاح! ({s["القرار"]}) 🎊</div>', unsafe_allow_html=True)
                    st.balloons() # تأثير الاحتفال
                else:
                    st.markdown(f'<div class="fail-text">😔 نعتذر، النتيجة: {s["القرار"]} 💔</div>', unsafe_allow_html=True)

                # عرض جدول المواد
                st.subheader("📊 تفاصيل النقاط")
                subjects = ['اللغة العربية', 'التربية الاسلامية', 'الرياضيات', 'الفرنسية', 
                            'العلوم', 'التاريخ والجغرافيا', 'التربية المدنية', 'التربية الفنية', 'الرياضة']
                
                # تحويل بيانات التلميذ لجدول بسيط
                scores_df = pd.DataFrame({
                    'المادة': subjects + ['المجموع'],
                    'النقطة': [s[sub] for sub in subjects] + [s['المجموع']]
                })
                st.table(scores_df)
            else:
                st.warning(f"لم يتم العثور على نتيجة لـ '{query}'. تأكد من كتابة الاسم أو الرقم بشكل صحيح.")
        else:
            st.info("يرجى إدخال الاسم أو الرقم أولاً.")

