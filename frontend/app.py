from flask import Flask, render_template
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import ast
from stats import make_stats
import os

app = Flask(__name__)

def get_data_path():
    # Получаем абсолютный путь к директории, где находится app.py
    base_dir = os.path.abspath(os.path.dirname(__file__))
    # Поднимаемся на уровень выше к корню проекта
    project_dir = os.path.dirname(base_dir)
    return os.path.join(project_dir, "dataset.txt")

def load_data():
    try:
        with open(get_data_path(), "r", encoding="utf-8") as file:
            lines = file.readlines()
        data = [ast.literal_eval(line.strip()) for line in lines]
        df = pd.DataFrame(data, columns=["tune", "category", "re"])
        return df
    except Exception as e:
        print(f"Error loading data: {e}")
        return pd.DataFrame(columns=["tune", "category", "re"])

def load_heatmap_data():
    try:
        data = make_stats()
        df = pd.DataFrame(data, columns=["category", "positive", "neutral", "negative"])
        return df
    except Exception as e:
        print(f"Error loading heatmap data: {e}")
        return pd.DataFrame(columns=["category", "positive", "neutral", "negative"])

@app.route('/')
def index():
    df = load_data()
    heatmap_df = load_heatmap_data()

    # Создание bar chart
    if not df.empty:
        category_counts = df['category'].value_counts()
        bar_fig = px.bar(category_counts, x=category_counts.index, y=category_counts.values, 
                        labels={'x': 'Категория', 'y': 'Количество'}, 
                        title='')
        bar_chart = bar_fig.to_html(full_html=False)
    else:
        bar_chart = "<p>Нет данных для отображения</p>"

    # Создание pie chart
    if not df.empty:
        pie_fig = px.pie(category_counts, values=category_counts.values, names=category_counts.index, 
                        title='')
        pie_chart = pie_fig.to_html(full_html=False)
    else:
        pie_chart = "<p>Нет данных для отображения</p>"

    # Создание heatmap
    if not heatmap_df.empty:
        heatmap_fig = px.imshow(
            heatmap_df.set_index('category'), 
            labels=dict(x="Параметры", y="Категории", color="Степень недовольства"),
            title="",
            color_continuous_scale=[[0, 'blue'], [1, 'red']],
            width=800,
            height=600
        )
        heatmap_chart = heatmap_fig.to_html(full_html=False)
    else:
        heatmap_chart = "<p>Нет данных для отображения</p>"

    return render_template('index.html', bar_chart=bar_chart, pie_chart=pie_chart, heatmap_chart=heatmap_chart)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8000)))