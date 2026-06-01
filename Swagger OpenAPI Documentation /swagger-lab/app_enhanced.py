from flask import Flask
from flask_restx import Api, Resource, fields, reqparse
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)

# Enhanced API configuration
api = Api(
    app,
    version='2.0',
    title='Book Library API',
    description='A comprehensive API for managing a book library with advanced features',
    doc='/docs',
    contact='admin@library.com',
    license='MIT'
)

ns = api.namespace('books', description='Book management operations')

books_db = [
    {'id': 1, 'title': '1984', 'author': 'George Orwell', 'year': 1949, 'isbn': '978-0451524935'},
    {'id': 2, 'title': 'To Kill a Mockingbird', 'author': 'Harper Lee', 'year': 1960, 'isbn': '978-0061120084'}
]

# Enhanced model with validation
book_model = api.model('Book', {
    'id': fields.Integer(readonly=True, description='Unique book identifier'),
    'title': fields.String(required=True, description='Book title', example='The Great Gatsby'),
    'author': fields.String(required=True, description='Author name', example='F. Scott Fitzgerald'),
    'year': fields.Integer(required=True, description='Publication year', min=1000, max=2100, example=1925),
    'isbn': fields.String(description='ISBN number', example='978-0743273565')
})

book_input_model = api.model('BookInput', {
    'title': fields.String(required=True, description='Book title', example='The Great Gatsby'),
    'author': fields.String(required=True, description='Author name', example='F. Scott Fitzgerald'),
    'year': fields.Integer(required=True, description='Publication year', example=1925),
    'isbn': fields.String(description='ISBN number', example='978-0743273565')
})

# TODO: Create a parser for query parameters
# Hint: Use reqparse.RequestParser() and add arguments for filtering
search_parser = reqparse.RequestParser()
# Add argument for 'author' (type=str, help text, location='args')
# Add argument for 'year' (type=int, help text, location='args')


@ns.route('/')
class BookList(Resource):
    @ns.doc('list_books', 
            params={
                'author': 'Filter by author name',
                'year': 'Filter by publication year'
            })
    @ns.marshal_list_with(book_model)
    @ns.expect(search_parser)
    def get(self):
        '''List all books with optional filtering'''
        # TODO: Implement filtering logic
        # 1. Parse arguments using search_parser.parse_args()
        # 2. Filter books_db based on provided parameters
        # 3. Return filtered results
        pass
    
    @ns.doc('create_book',
            responses={
                201: 'Book created successfully',
                400: 'Validation error'
            })
    @ns.expect(book_input_model, validate=True)
    @ns.marshal_with(book_model, code=201)
    def post(self):
        '''Create a new book with validation'''
        # TODO: Implement with validation
        # Check if book with same title and author exists
        # If exists, use api.abort(400, "Book already exists")
        pass


@ns.route('/<int:id>')
@ns.param('id', 'The book identifier')
class Book(Resource):
    @ns.doc('get_book',
            responses={
                200: 'Success',
                404: 'Book not found'
            })
    @ns.marshal_with(book_model)
    def get(self, id):
        '''Fetch a specific book by ID'''
        for book in books_db:
            if book['id'] == id:
                return book
        api.abort(404, f"Book {id} not found")
    
    @ns.doc('update_book',
            responses={
                200: 'Book updated successfully',
                404: 'Book not found'
            })
    @ns.expect(book_input_model, validate=True)
    @ns.marshal_with(book_model)
    def put(self, id):
        '''Update an existing book'''
        for book in books_db:
            if book['id'] == id:
                book.update(api.payload)
                return book
        api.abort(404, f"Book {id} not found")
    
    @ns.doc('delete_book',
            responses={
                204: 'Book deleted successfully',
                404: 'Book not found'
            })
    def delete(self, id):
        '''Delete a book from the library'''
        for i, book in enumerate(books_db):
            if book['id'] == id:
                books_db.pop(i)
                return '', 204
        api.abort(404, f"Book {id} not found")


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
search_parser.add_argument('author', type=str, help='Filter by author', location='args')
search_parser.add_argument('year', type=int, help='Filter by year', location='args')
args = search_parser.parse_args()
result = books_db

if args['author']:
    result = [b for b in result if args['author'].lower() in b['author'].lower()]
if args['year']:
    result = [b for b in result if b['year'] == args['year']]

return result
