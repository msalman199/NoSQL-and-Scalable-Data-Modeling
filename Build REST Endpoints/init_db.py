import sqlite3

def init_database():
    """
    Initialize SQLite database with books table.
    Creates the database file and schema if not exists.
    """
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    
    # TODO: Create books table with columns:
    # - id (INTEGER PRIMARY KEY AUTOINCREMENT)
    # - title (TEXT NOT NULL)
    # - author (TEXT NOT NULL)
    # - year (INTEGER)
    # - isbn (TEXT UNIQUE)
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            -- Add your column definitions here
        )
    ''')
    
    # TODO: Insert 3 sample books for testing
    sample_books = [
        # Add tuples with (title, author, year, isbn)
    ]
    
    # cursor.execute("INSERT INTO books (title, author, year, isbn) VALUES (?, ?, ?, ?)", sample_books[0])
    
    conn.commit()
    conn.close()
    print("Database initialized successfully!")

if __name__ == '__main__':
    init_database()
