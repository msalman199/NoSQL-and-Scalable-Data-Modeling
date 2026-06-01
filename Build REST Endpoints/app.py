from flask import Flask, request, jsonify
from flask_cors import CORS
import db_operations

app = Flask(__name__)
CORS(app)

# GET /api/books - Retrieve all books
@app.route('/api/books', methods=['GET'])
def get_books():
    """
    Endpoint to retrieve all books.
    
    Returns:
        JSON array of books with 200 status
    """
    # TODO: Call db_operations.get_all_books()
    # TODO: Return jsonify(books) with status 200
    pass

# GET /api/books/<id> - Retrieve single book
@app.route('/api/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    """
    Endpoint to retrieve a specific book.
    
    Args:
        book_id: Book ID from URL path
    
    Returns:
        JSON object with book data or 404 error
    """
    # TODO: Call db_operations.get_book_by_id(book_id)
    # TODO: If book exists, return jsonify(book), 200
    # TODO: If not found, return jsonify({'error': 'Book not found'}), 404
    pass

# POST /api/books - Create new book
@app.route('/api/books', methods=['POST'])
def create_book():
    """
    Endpoint to create a new book.
    
    Expects JSON body with: title, author, year, isbn
    
    Returns:
        JSON with new book ID and 201 status
    """
    # TODO: Get JSON data from request.get_json()
    # TODO: Validate required fields exist
    # TODO: Call db_operations.create_book()
    # TODO: Return jsonify({'id': new_id, 'message': 'Book created'}), 201
    # TODO: Handle errors with 400 status
    pass

# PUT /api/books/<id> - Update existing book
@app.route('/api/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    """
    Endpoint to update an existing book.
    
    Args:
        book_id: Book ID from URL path
    
    Expects JSON body with: title, author, year, isbn
    
    Returns:
        Success message or 404/400 error
    """
    # TODO: Get JSON data
    # TODO: Validate fields
    # TODO: Call db_operations.update_book()
    # TODO: Return appropriate status code
    pass

# DELETE /api/books/<id> - Delete book
@app.route('/api/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    """
    Endpoint to delete a book.
    
    Args:
        book_id: Book ID from URL path
    
    Returns:
        Success message or 404 error
    """
    # TODO: Call db_operations.delete_book()
    # TODO: Return jsonify({'message': 'Book deleted'}), 200 if successful
    # TODO: Return 404 if book not found
    pass

# Health check endpoint
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
