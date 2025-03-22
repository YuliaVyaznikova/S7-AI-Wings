from flask import Flask, render_template, jsonify
from collections import Counter

app = Flask(__name__)

# Статические данные для демонстрации
SAMPLE_DATA = [
    {"category": "Багаж", "tune": "negative", "re": "Потеряли багаж"},
    {"category": "Сервис", "tune": "positive", "re": "Отличное обслуживание"},
    {"category": "Питание", "tune": "neutral", "re": "Стандартное питание"},
    {"category": "Багаж", "tune": "negative", "re": "Долгая выдача багажа"},
    {"category": "Сервис", "tune": "positive", "re": "Вежливый персонал"},
    {"category": "Комфорт", "tune": "positive", "re": "Удобные кресла"},
]

SAMPLE_HEATMAP = [
    {"category": "Багаж", "positive": 0.2, "neutral": 0.3, "negative": 0.5},
    {"category": "Сервис", "positive": 0.7, "neutral": 0.2, "negative": 0.1},
    {"category": "Питание", "positive": 0.4, "neutral": 0.4, "negative": 0.2},
    {"category": "Комфорт", "positive": 0.6, "neutral": 0.3, "negative": 0.1},
]

@app.route('/api/data')
def get_data():
    try:
        categories = [item['category'] for item in SAMPLE_DATA]
        category_counts = Counter(categories)
        
        return jsonify({
            'categories': dict(category_counts),
            'heatmap': SAMPLE_HEATMAP
        })
    except Exception as e:
        return jsonify({
            'categories': {},
            'heatmap': [],
            'error': str(e)
        }), 500

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)