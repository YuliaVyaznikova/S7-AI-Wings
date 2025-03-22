from flask import Flask, render_template, jsonify
import ast
from stats import make_stats
from collections import Counter

app = Flask(__name__)

def load_data():
    try:
        with open("dataset.txt", "r", encoding="utf-8") as file:
            lines = file.readlines()
        data = [ast.literal_eval(line.strip()) for line in lines]
        return data
    except Exception as e:
        print(f"Error loading data: {e}")
        return []

def load_heatmap_data():
    try:
        return make_stats()
    except Exception as e:
        print(f"Error loading heatmap data: {e}")
        return []

@app.route('/api/data')
def get_data():
    data = load_data()
    categories = [item['category'] for item in data]
    category_counts = Counter(categories)
    
    heatmap_data = load_heatmap_data()
    
    return jsonify({
        'categories': dict(category_counts),
        'heatmap': heatmap_data
    })

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)