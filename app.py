from flask import Flask, jsonify, request
import json

app = Flask(__name__)

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

def init_db():
    try:
        with open('books.json', 'r') as f:
            db = json.load(f)
    except FileNotFoundError:
        db = {'books': []}
        with open('books.json', 'w') as f:
            json.dump(db, f)

def get_db():
    with open('books.json', 'r') as f:
        return json.load(f)

def save_db(db):
    with open('books.json', 'w') as f:
        json.dump(db, f)

@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/books', methods=['GET'])
def get_books():
    db = get_db()
    books = db['books']
    return jsonify([{'id': book['id'], 'title': book['title'], 'author': book['author'], 'votes': book['votes'], 'image': book['image'], 'genre': book['genre']} for book in books])

@app.route('/books/<int:book_id>/vote', methods=['POST'])
def vote_book(book_id):
    db = get_db()
    books = db['books']
    for book in books:
        if book['id'] == book_id:
            book['votes'] += 1
            save_db(db)
            return '', 204
    return '', 404

@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    db = get_db()
    books = db['books']
    for book in books:
        if book['id'] == book_id:
            books.remove(book)
            save_db(db)
            return '', 204
    return '', 404

@app.route('/books', methods=['POST'])
def create_book():
    db = get_db()
    books = db['books']
    new_book = {
        'id': len(books) + 1,
        'title': request.json['title'],
        'author': request.json['author'],
        'votes': request.json.get('votes', 0),
        'image': request.json.get('image', ''),
        'genre': request.json.get('genre', [])  
    }
    books.append(new_book)
    save_db(db)
    return jsonify(new_book), 201

@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    db = get_db()
    books = db['books']
    for book in books:
        if book['id'] == book_id:
            return jsonify(book)
    return '', 404

@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    db = get_db()
    books = db['books']
    for book in books:
        if book['id'] == book_id:
            book['title'] = request.json.get('title', book['title'])
            book['author'] = request.json.get('author', book['author'])
            book['votes'] = request.json.get('votes', book['votes'])
            book['image'] = request.json.get('image', book['image'])
            book['genre'] = request.json.get('genre', book.get('genre', []))  
            save_db(db)
            return jsonify(book)
    return '', 404

if __name__ == '__main__':
    init_db()
    app.run(debug=True)