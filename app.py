from flask import Flask, render_template, jsonify
import requests

app = Flask(__name__)

# Главная страница с HTML-шаблоном
@app.route('/')
def index():
    try:
        # Запрос к API для получения случайной цитаты
        response = requests.get('https://zenquotes.io/api/random', timeout=5)
        response.raise_for_status()  # Проверка успешности запроса
        data = response.json()  # Преобразуем ответ в JSON
        quote_data = data[0]  # Извлекаем первый элемент из массива
        quote = quote_data['q']  # Цитата
        author = quote_data['a']  # Автор
    except Exception as e:
        print(f"Error fetching quote: {e}")
        quote = "Could not fetch a quote at this time."
        author = "Anonymous"

    return render_template('index.html', quote=quote, author=author)

# API для получения новой цитаты без перезагрузки
@app.route('/api/quote', methods=['GET'])
def get_new_quote():
    try:
        # Запрос к API для получения новой цитаты
        response = requests.get('https://zenquotes.io/api/random', timeout=5)
        response.raise_for_status()  # Проверка успешности запроса
        data = response.json()  # Преобразуем ответ в JSON
        quote_data = data[0]  # Извлекаем первый элемент из массива
        return jsonify({
            "content": quote_data['q'],  # Извлекаем текст цитаты
            "author": quote_data['a']    # Извлекаем имя автора
        })
    except Exception as e:
        print(f"Error fetching quote: {e}")
        return jsonify({"content": "Could not fetch a quote at this time.", "author": "Anonymous"})

if __name__ == '__main__':
    app.run(debug=True)
