from flask import Flask, render_template_string, request
import pandas as pd
import os

app = Flask(__name__)

# اسم الملف الذي سيرفعه المدير
EXCEL_FILE = 'results.xlsx'

INDEX_HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>بوابة نتائج التلاميذ</title>
    <style>
        :root { --p: #2563eb; --s: #10b981; --d: #ef4444; --bg: #f1f5f9; }
        body { font-family: 'Segoe UI', Tahoma, sans-serif; background: var(--bg); margin: 0; padding: 15px; display: flex; justify-content: center; }
        .card { background: white; width: 100%; max-width: 600px; padding: 25px; border-radius: 20px; box-shadow: 0 10px 25px rgba(0,0,0,0.1); }
        h1 { text-align: center; color: #1e293b; margin-bottom: 25px; font-size: 1.6rem; border-bottom: 2px solid var(--p); padding-bottom: 10px; }
        .search-form { display: flex; flex-direction: column; gap: 12px; margin-bottom: 25px; }
        .input-hint { font-size: 0.85rem; color: #64748b; margin-bottom: -8px; margin-right: 5px; }
        input { padding: 14px; border: 2px solid #e2e8f0; border-radius: 12px; font-size: 1rem; outline: none; transition: 0.2s; }
        input:focus { border-color: var(--p); }
        button { padding: 14px; background: var(--p); color: white; border: none; border-radius: 12px; font-weight: bold; cursor: pointer; font-size: 1.1rem; }
        button:hover { background: #1e40af; }
        .res-container { animation: fadeIn 0.5s; border-top: 2px solid #f1f5f9; padding-top: 20px; }
        .info-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin: 15px 0; }
        .info-item { background: #f8fafc; padding: 12px; border-radius: 10px; text-align: center; border: 1px solid #e2e8f0; }
        .badge { padding: 15px; border-radius: 12px; text-align: center; font-weight: bold; font-size: 1.2rem; margin: 15px 0; }
        .pass { background: #dcfce7; color: #166534; border: 1px solid #bbf7d0; }
        .fail { background: #fee2e2; color: #991b1b; border: 1px solid #fecaca; }
        .table-wrap { overflow-x: auto; margin-top: 15px; }
        table { width: 100%; border-collapse: collapse; min-width: 400px; }
        th, td { padding: 12px; border-bottom: 1px solid #f1f5f9; text-align: center; }
        th { background: #f8fafc; color: #64748b; font-size: 0.9rem; }
        .error { color: var(--d); text-align: center; font-weight: bold; background: #fff1f2; padding: 10px; border-radius: 8px; }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
    </style>
</head>
<body>
    <div class="card">
        <h1>🎓 استعلام عن النتائج</h1>
        <form class="search-form" method="POST">
            <span class="input-hint">ابحث برقمك الخاص أو اسمك الكامل:</span>
            <input type="text" name="query" placeholder="أدخل الرقم أو الاسم هنا..." required>
            <button type="submit">بحث عن النتيجة</button>
        </form>

        {% if error %} <div class="error">⚠️ {{ error }}</div> {% endif %}

        {% if s %}
        <div class="res-container">
            <h2 style="text-align:center; color:var(--p);">{{ s['الاسم'] }}</h2>
            <div class="info-grid">
                <div class="info-item"><small>المعدل</small><br><strong>{{ s['المعدل'] }}</strong></div>
                <div class="info-item"><small>الرتبة</small><br><strong>{{ s['الرتبة'] }}</strong></div>
            </div>

            {% if "ناجح" in s['القرار'] %}
                <div class="badge pass">🎉 ألف مبروك النجاح! ({{ s['القرار'] }}) 🥳</div>
            {% else %}
                <div class="badge fail">😔 نعتذر، النتيجة: {{ s['القرار'] }} 💔</div>
            {% endif %}

            <div class="table-wrap">
                <table>
                    <thead><tr><th>المادة</th><th>النقطة</th></tr></thead>
                    <tbody>
                        {% for m in ['اللغة العربية', 'التربية الاسلامية', 'الرياضيات', 'الفرنسية', 'العلوم', 'التاريخ والجغرافيا', 'التربية المدنية', 'التربية الفنية', 'الرياضة'] %}
                        <tr><td>{{ m }}</td><td>{{ s[m] }}</td></tr>
                        {% endfor %}
                        <tr style="background:#f8fafc; font-weight:bold;"><td>المجموع</td><td>{{ s['المجموع'] }}</td></tr>
                    </tbody>
                </table>
            </div>
        </div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    s_data, error = None, None
    if request.method == 'POST':
        search_val = request.form.get('query').strip()
        
        if not os.path.exists(EXCEL_FILE):
            error = "خطأ: ملف النتائج غير متوفر حالياً."
        else:
            try:
                df = pd.read_excel(EXCEL_FILE)
                # منطق البحث: (هل القيمة تساوي الرقم) أو (هل القيمة تساوي الاسم)
                match = df[(df['الرقم'].astype(str).str.strip() == search_val) | 
                           (df['الاسم'].str.strip() == search_val)]
                
                if not match.empty:
                    # نأخذ أول نتيجة مطابقة في حال تكرار الأسماء
                    s_data = match.iloc.to_dict()
                else:
                    error = f"عذراً، لم نجد أي نتيجة مطابقة لـ '{search_val}'."
            except Exception as e:
                error = "حدث خطأ في النظام، يرجى المحاولة لاحقاً."
                
    return render_template_string(INDEX_HTML, s=s_data, error=error)

if __name__ == '__main__':
    app.run(debug=True)
