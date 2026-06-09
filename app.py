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
    
    /* تنسيق صندوق بطاقات النتائج لتظهر بوضوح (نص داكن وخلفية مريحة) */
    .metric-container { background-color: #f8fafc; border: 1px solid #e2e8f0; padding: 15px; border-radius: 14px; text-align: center; box-shadow: 0 1px 3px rgba(0,0,0,0.05); margin-bottom: 10px; }
    .metric-title { color: #64748b; font-size: 14px; margin-bottom: 5px; font-weight: 600; }
    .metric-value { color: #0f172a; font-size: 26px; font-weight: bold; }
    
    /* تنسيق علامات التبويب والخانات لتكون واضحة وجذابة على الهاتف */
    button[data-baseweb="tab"] { font-size: 16px !important; font-weight: bold !important; padding: 12px 20px !important; }
    
    /* تنسيق رسائل النجاح والرسوب بخلفيات ناعمة ونصوص واضحة */
    .success-box { color: #15803d; background-color: #f0fdf4; border: 1px solid #bbf7d0; padding: 18px; border-radius: 14px; text-align: center; font-size: 18px; font-weight: bold; margin: 15px 0; }
    .fail-box { color: #b91c1c; background-color: #fef2f2; border: 1px solid #fecaca; padding: 18px; border-radius: 14px; text-align: center; font-size: 18px; font-weight: bold; margin: 15px 0; }
    
    /* تحسين جداول البيانات وعرضها على الجوال */
    .stTable { width: 100% !important; border-radius: 10px; overflow: hidden; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎓 بوابة نتائج التلاميذ")
st.write("استخدم الاسم أو الرقم للاستعلام عن النتيجة")

# اسم ملف البيانات الثابت
EXCEL_FILE = 'results.xlsx'

# 3. التحقق من وجود الملف
if not os.path.exists(EXCEL_FILE):
    st.error("⚠️ ملف النتائج (results.xlsx) غير موجود. يرجى رفعه في GitHub.")
else:
    try:
        df = pd.read_excel(EXCEL_FILE)
        
        # مدخلات البحث (الاسم أو الرقم)
        query = st.text_input("أدخل رقم التلميذ أو الاسم الكامل:", placeholder="مثال: 10 أو أدو ولد سعيدو")
        
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
                        
                        # جلب درجات المواد الخاصة بالامتحان الأول (ملحقة برقم 1)
                        for sub in subjects_list:
                            labels1.append(sub)
                            values1.append(format_value(s.get(f'{sub} 1')))
                        
                        # إضافة الإجماليات والمؤشرات الخاصة بالامتحان الأول
                        summary_fields1 = ['المجموع 1', 'المعدل 1', 'الرتبة 1', 'القرار 1']
                        summary_labels1 = ['المجموع', 'المعدل', 'الرتبة', 'القرار']
                        
                        for field, label in zip(summary_fields1, summary_labels1):
                            labels1.append(label)
                            values1.append(format_value(s.get(field)))
                            
                        # عرض الجدول
                        st.table(pd.DataFrame({'المادة / البيان': labels1, 'النتيجة': values1}))
                        
                        # عرض رسالة القرار بالأسفل للتنسيق البصري
                        dec1 = str(s.get('القرار 1', ''))
                        if "ناجح" in dec1 or "مقبول" in dec1:
                            st.markdown(f'<div class="success-box">🎉 نتيجة الامتحان الأول: {dec1} </div>', unsafe_allow_html=True)
                        elif "راسب" in dec1 or "مكرر" in dec1:
                            st.markdown(f'<div class="fail-box">😔 نتيجة الامتحان الأول: {dec1} </div>', unsafe_allow_html=True)

                    # --- خانة الامتحان الثاني ---
                    with tab2:
                        st.subheader("📊 كشف درجات الامتحان الثاني")
                        labels2 = []
                        values2 = []
                        
                        # جلب درجات المواد الخاصة بالامتحان الثاني (ملحقة برقم 2)
                        for sub in subjects_list:
                            labels2.append(sub)
                            values2.append(format_value(s.get(f'{sub} 2')))
                        
                        # إضافة الإجماليات والمؤشرات الخاصة بالامتحان الثاني
                        summary_fields2 = ['المجموع 2', 'المعدل 2', 'الرتبة 2', 'القرار 2']
                        summary_labels2 = ['المجموع', 'المعدل', 'الرتبة', 'القرار']
                        
                        for field, label in zip(summary_fields2, summary_labels2):
                            labels2.append(label)
                            values2.append(format_value(s.get(field)))
                            
                        st.table(pd.DataFrame({'المادة / البيان': labels2, 'النتيجة': values2}))
                        
                        dec2 = str(s.get('القرار 2', ''))
                        if "ناجح" in dec2 or "مقبول" in dec2:
                            st.markdown(f'<div class="success-box">🎉 نتيجة الامتحان الثاني: {dec2} </div>', unsafe_allow_html=True)
                        elif "راسب" in dec2 or "مكرر" in dec2:
                            st.markdown(f'<div class="fail-box">😔 نتيجة الامتحان الثاني: {dec2} </div>', unsafe_allow_html=True)

                    # --- خانة الامتحان الأخير (الثالث) ---
                    with tab3:
                        st.subheader("📊 كشف درجات الامتحان الأخير")
                        labels3 = []
                        values3 = []
                        
                        # جلب درجات المواد الخاصة بالامتحان الأخير (ملحقة برقم 3)
                        for sub in subjects_list:
                            labels3.append(sub)
                            values3.append(format_value(s.get(f'{sub} 3')))
                        
                        # إضافة الإجماليات والمؤشرات الخاصة بالامتحان الأخير بالإضافة إلى (المعدل العام السنوي والقرار النهائي للعام) كما طلبت
                        summary_fields3 = ['المجموع 3', 'المعدل 3', 'الرتبة 3', 'القرار 3', 'المعدل العام', 'الرتبة العامة', 'القرار العام']
                        summary_labels3 = ['المجموع', 'المعدل', 'الرتبة', 'القرار', 'المعدل العام للسنة', 'الرتبة السنوية العامة', 'القرار السنوي النهائي']
                        
                        for field, label in zip(summary_fields3, summary_labels3):
                            labels3.append(label)
                            values3.append(format_value(s.get(field)))
                            
                        st.table(pd.DataFrame({'المادة / البيان': labels3, 'النتيجة': values3}))
                        
                        dec3 = str(s.get('القرار العام', ''))
                        if "ناجح" in dec3 or "منتقل" in dec3:
                            st.markdown(f'<div class="success-box">🏆 النتيجة السنوية النهائية: {dec3} 🎈</div>', unsafe_allow_html=True)
                            st.balloons()
                        elif "راسب" in dec3 or "مكرر" in dec3:
                            st.markdown(f'<div class="fail-box">😔 النتيجة السنوية النهائية: {dec3} 💔</div>', unsafe_allow_html=True)
                                
                else:
                    st.error(f"❌ لم يتم العثور على نتيجة لـ '{query}'.")
            else:
                st.info("يرجى كتابة الاسم أو الرقم أولاً.")
    except Exception as e:
        st.error(f"حدث خطأ في قراءة البيانات: {e}")
