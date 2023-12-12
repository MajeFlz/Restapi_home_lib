from flask import jsonify, abort, request, Blueprint

request_api = Blueprint('request_api', __name__)
def get_blueprint():
    return request_api

books = [
    {'id': 1,'title': "Зов Ктулху",'author': "Говард Филлипс Лавкрафт",'genre': "Ужасы",'year': "1926"},
    {'id': 2,'title': "Туман",'author': "Стивен Кинг",'genre': "Фантастика",'year': "1980"},
    {'id': 3,'title': "Алгоритмы и структуры данных",'author': "Никлаус Вирт",'genre': "Информатика",'year': "1985"}
]

@request_api.route('/books', methods=['GET'])
def get_books():
    if books:
        return jsonify(books)
    else:
        return jsonify({"error": "Книги не найдены"}), 404

@request_api.route('/books', methods=['POST'])
def create_book():
    if not request.get_json():
        return jsonify({"error": "Неверные данные"}), 400
    data = request.get_json(force=True)

    if not data.get('title') or not data.get('author'):
        return jsonify({"error": "Неверные данные"}), 400

    book_id = len(books) + 1
    data['id'] = book_id
    books.append(data)
    return jsonify(data), 201

@request_api.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = next((b for b in books if b['id'] == book_id), None)
    if book:
        return jsonify(book)
    else:
        return jsonify({"error": "Книга не найдена"}), 404

@request_api.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    if not request.get_json():
        abort(400)
    data = request.get_json(force=True)

    book = next((b for b in books if b['id'] == book_id), None)
    if book:
        book.update(data)
        return jsonify(book)
    else:
        return jsonify({"error": "Книга не найдена"}), 404

@request_api.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    global books
    book_to_delete = next((book for book in books if book['id'] == book_id), None)
    if book_to_delete:
        books.remove(book_to_delete)
        return jsonify(book_to_delete), 204
    else:
        return jsonify({"error": "Книга не найдена"}), 404

