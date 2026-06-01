import sqlite3
from typing import List, Dict, Optional

DATABASE = 'library.db'

def get_db_connection():
    """Establish database connection with row factory."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def get_all_books() -> List[Dict]:
    """
    Retrieve all books from database.
    
    Returns:
        List of dictionaries containing book data
    """
    # TODO: Connect to database
    # TODO: Execute SELECT query to get all books
    # TODO: Convert rows to list of dictionaries
    # TODO: Close connection and return results
    pass

def get_book_by_id(book_id: int) -> Optional[Dict]:
    """
    Retrieve a single book by ID.
    
    Args:
        book_id: The book's unique identifier
    
    Returns:
        Dictionary with book data or None if not found
    """
    # TODO: Implement query with WHERE clause
    pass

def create_book(title: str, author: str, year: int, isbn: str) -> int:
    """
    Insert a new book into database.
    
    Args:
        title: Book title
        author: Book author
        year: Publication year
        isbn: ISBN number
    
    Returns:
        ID of newly created book
    """
    # TODO: Execute INSERT statement
    # TODO: Return lastrowid
    pass

def update_book(book_id: int, title: str, author: str, year: int, isbn: str) -> bool:
    """
    Update existing book record.
    
    Args:
        book_id: Book ID to update
        title, author, year, isbn: New values
    
    Returns:
        True if successful, False otherwise
    """
    # TODO: Execute UPDATE statement with WHERE clause
    # TODO: Check rowcount to verify update
    pass

def delete_book(book_id: int) -> bool:
    """
    Delete a book from database.
    
    Args:
        book_id: Book ID to delete
    
    Returns:
        True if successful, False otherwise
    """
    # TODO: Execute DELETE statement
    pass
