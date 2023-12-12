from flask import jsonify, abort, request, Blueprint
from models import Book, db

request_api = Blueprint('request_api', __name__)
def get_blueprint():
    return request_api

@request_api.route('/books', methods=['GET'])
def get_books():
    books = Book.query.all()
    if books:
        books_data = [{"id": book.id, "title": book.title, "author": book.author, "genre": book.genre, "year": book.year} for book in books]
        return jsonify(books_data)
    else:
        return jsonify({"error": "Книги не найдены"}), 404

@request_api.route('/books', methods=['POST'])
def create_book():
    data = request.get_json(force=True)
    if not data.get('title') or not data.get('author'):
        return jsonify({"error": "Неверные данные"}), 400

    new_book = Book(title=data['title'], author=data['author'], genre=data.get('genre'), year=data.get('year'))
    db.session.add(new_book)
    db.session.commit()

    return jsonify({"message": "Книга создана успешно"}), 201

@request_api.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = Book.query.get(book_id)
    if book:
        return jsonify({"id": book.id, "title": book.title, "author": book.author, "genre": book.genre, "year": book.year})
    else:
        return jsonify({"error": "Книга не найдена"}), 404

@request_api.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    data = request.get_json(force=True)
    book = Book.query.get(book_id)

    if not book:
        return jsonify({"error": "Книга не найдена"}), 404

    book.title = data.get('title', book.title)
    book.author = data.get('author', book.author)
    book.genre = data.get('genre', book.genre)
    book.year = data.get('year', book.year)

    db.session.commit()

    return jsonify({"message": "Книга успешно обновлена"}), 200

@request_api.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    book = Book.query.get(book_id)
    if book:
        db.session.delete(book)
        db.session.commit()
        return jsonify({"message": "Книга успешно удалена"}), 200
    else:
        return jsonify({"error": "Книга не найдена"}), 404
