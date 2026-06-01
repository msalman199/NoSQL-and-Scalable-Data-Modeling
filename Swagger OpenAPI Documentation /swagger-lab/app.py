from flask import Flask, request
from flask_restx import Api, Resource, fields
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)

# TODO: Initialize the API with custom documentation
# Hint: Use Api() with title, version, description, and doc parameters
api = Api(
    app,
    version='1.0',
    title='Book Library API',
    description='A simple API for managing a book library',
    doc='/docs'
)

# Create namespace for organizing endpoints
ns = api.namespace('books', description='Book operations')

# In-memory database
books_db = [
    {'id': 1, 'title': '1984', 'author': 'George Orwell', 'year': 1949},
    {'id': 2, 'title': 'To Kill a Mockingbird', 'author': 'Harper Lee', 'year': 1960}
]

# TODO: Define the book model for Swagger documentation
# Hint: Use api.model() with fields for id, title, author, year
book_model = api.model('Book', {
    'id': fields.Integer(required=True, description='Book ID'),
    'title': fields.String(required=True, description='Book title'),
    'author': fields.String(required=True, description='Book author'),
    'year': fields.Integer(required=True, description='Publication year')
})

# TODO: Create input model without id field (for POST requests)
book_input_model = api.model('BookInput', {
    # Add fields: title, author, year
})


@ns.route('/')
class BookList(Resource):
    @ns.doc('list_books')
    @ns.marshal_list_with(book_model)
    def get(self):
        '''List all books'''
        return books_db
    
    @ns.doc('create_book')
    @ns.expect(book_input_model)
    @ns.marshal_with(book_model, code=201)
    def post(self):
        '''Create a new book'''
        # TODO: Implement book creation logic
        # 1. Get JSON data from api.payload
        # 2. Generate new ID
        # 3. Add book to books_db
        # 4. Return the new book
        pass


@ns.route('/<int:id>')
@ns.response(404, 'Book not found')
@ns.param('id', 'The book identifier')
class Book(Resource):
    @ns.doc('get_book')
    @ns.marshal_with(book_model)
    def get(self, id):
        '''Fetch a book by ID'''
        # TODO: Find and return book by id
        # Return 404 if not found using api.abort(404, "Book not found")
        pass
    
    @ns.doc('delete_book')
    @ns.response(204, 'Book deleted')
    def delete(self, id):
        '''Delete a book'''
        # TODO: Implement delete logic
        # Return empty response with 204 status
        pass
    
    @ns.doc('update_book')
    @ns.expect(book_input_model)
    @ns.marshal_with(book_model)
    def put(self, id):
        '''Update a book'''
        # TODO: Implement update logic
        # Find book, update fields, return updated book
        pass


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
