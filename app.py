import streamlit as st
import pandas as pd
import os

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة نتائج التلاميذ", page_icon="🎓", layout="centered")

# 2. تصميم CSS مخصص (متوافق مع اللغة العربية)
st.markdown("""
    <style>
    .stApp { direction: rtl; text-align: right; }
    div.stButton > button { width: 100%; border-radius: 10px; background-color: #2563eb; color: white; height: 3em; font-weight: bold; }
    .success-text { color: #166534; background-color: #dcfce7; padding: 20px; border-radius: 15px; text-align: center; font-size: 20px; font-weight: bold; margin: 10px 0; }
    .fail-text { color: #991b1b; background-color: #fee2e2; padding: 20px; border-radius: 15px; text-align: center; font-size: 20px; font-weight: bold; margin: 10px 0; }
    .stMetric { background: #f1f5f9; padding: 10px; border-radius: 10px; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎓 بوابة نتائج التلاميذ")
st.write("استخدم الاسم أو الرقم للاستعلام عن النتيجة")

# اسم ملف المدير
EXCEL_FILE = 'results.xlsx'

# 3. التحقق من وجود الملف
if not os.path.exists(EXCEL_FILE):
    st.error("⚠️ ملف النتائج (results.xlsx) غير موجود. يرجى رفعه في GitHub.")
else:
    try:
        df = pd.read_excel(EXCEL_FILE)
        
        # حقل البحث
        query = st.text_input("أدخل رقم التلميذ أو الاسم الكامل:", placeholder="مثال: 101 أو أحمد محمد")
        
        if st.button("استعلام"):
            if query:
                # تنظيف النص وتغيير نوع البيانات للبحث
                q = str(query).strip()
                match = df[(df['الرقم'].astype(str).str.strip() == q) | 
                           (df['الاسم'].str.strip() == q)]
                
                if not match.empty:
                    s = match.iloc[0].to_dict() # أخذ أول تلميذ مطابق
                    
                    st.divider()
                    st.header(f"مرحباً، {s.get('الاسم', 'أيها التلميذ')}")
                    
                    # عرض المعدل والرتبة في الأعلى كبطاقات سريعة
                    col1, col2 = st.columns(2)
                    col1.metric("المعدل العام", s.get('المعدل العام', 'غير متوفر'))
                    col2.metric("الرتبة", s.get('الرتبة', 'غير متوفر'))
                    
                    # القرار والاحتفال
                    قرار = str(s.get('القرار', ''))
                    if "ناجح" in قرار:
                        st.markdown(f'<div class="success-text">🎉 مبروك النجاح! ({قرار}) 🎊</div>', unsafe_allow_html=True)
                        st.balloons()
                    elif "راسب" in قرار or "مكرر" in قرار:
                        st.markdown(f'<div class="fail-text">😔 نعتذر، النتيجة: {قرار} 💔</div>', unsafe_allow_html=True)
                    
                    # 4. عرض تفاصيل التلميذ بناءً على العناوين الجديدة
                    st.subheader("📊 تفاصيل وبينات التلميذ")
                    
                    # قائمة العناوين الجديدة المطلوبة
                    expected_columns = [
                        'الرقم', 'الاسم', 'معدل الامتحان الأول', 
                        'معدل الامتحان الثاني', 'معدل الامتحان الأخير', 
                        'المعدل العام', 'الرتبة', 'القرار'
                    ]
                    
                    available_labels = []
                    available_values = []

                    for col in expected_columns:
                        if col in s: # التأكد من وجود العمود في ملف الإكسل
                            available_labels.append(col)
                            available_values.append(s[col])
                    
                    if available_labels:
                        details_df = pd.DataFrame({
                            'البيان': available_labels,
                            'القيمة': available_values
                        })
                        st.table(details_df)
                    else:
                        st.warning("⚠️ لم يتم العثور على الأعمدة المطلوبة. تأكد من مطابقة أسماء الأعمدة في ملف الإكسل تماماً.")
                else:
                    st.error(f"❌ لم يتم العثور على نتيجة لـ '{query}'.")
            else:
                st.info("يرجى كتابة الاسم أو الرقم أولاً.")
    except Exception as e:
        st.error(f"حدث خطأ في قراءة البيانات: {e}")
