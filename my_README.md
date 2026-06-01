# 🚀 Build REST Endpoints with Flask & SQLite

<p align="center">
  <img src="https://img.shields.io/badge/Lab-REST_API_Development-blue?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Python-3.x-yellow?style=for-the-badge&logo=python" />
  <img src="https://img.shields.io/badge/Flask-Web_Framework-black?style=for-the-badge&logo=flask" />
  <img src="https://img.shields.io/badge/SQLite-Database-blue?style=for-the-badge&logo=sqlite" />
  <img src="https://img.shields.io/badge/Linux-Ubuntu-orange?style=for-the-badge&logo=ubuntu" />
</p>

---

# 📖 Overview

In this lab, you will build a complete **RESTful API** using **Python Flask** and **SQLite**. The API will manage a collection of books and support full CRUD (Create, Read, Update, Delete) operations.

---

# 🎯 Learning Objectives

By completing this lab, you will be able to:

✅ Develop RESTful APIs using Flask

✅ Implement CRUD operations

✅ Connect APIs to SQLite databases

✅ Handle JSON requests and responses

✅ Return proper HTTP status codes

✅ Test APIs using curl commands

---

# 📋 Prerequisites

Before starting this lab, you should have:

- Basic understanding of HTTP methods (GET, POST, PUT, DELETE)
- Familiarity with Python programming
- Knowledge of JSON data format
- Basic Linux command line skills
- Understanding of database concepts

---

# 🛠️ Environment Setup

## 🔹 Update Package Manager

```bash
sudo apt update
```

---

## 🔹 Install Python & Required Packages

```bash
sudo apt install -y python3 python3-pip python3-venv
```

---

## 🔹 Create Project Directory

```bash
mkdir ~/rest-api-lab
cd ~/rest-api-lab
```

---

## 🔹 Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 🔹 Install Flask Dependencies

```bash
pip install flask flask-cors
```

---

# 🗄️ Task 1: Create Database Schema

## ✨ Step 1: Create Database Initialization Script

```bash
nano init_db.py
```

### Add the Following Code

```python
import sqlite3

def init_database():
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            year INTEGER,
            isbn TEXT UNIQUE
        )
    ''')

    sample_books = [
        ("Clean Code", "Robert C. Martin", 2008, "9780132350884"),
        ("Python Crash Course", "Eric Matthes", 2019, "9781593279288"),
        ("Fluent Python", "Luciano Ramalho", 2022, "9781492056355")
    ]

    cursor.executemany(
        "INSERT OR IGNORE INTO books(title, author, year, isbn) VALUES (?, ?, ?, ?)",
        sample_books
    )

    conn.commit()
    conn.close()

    print("Database initialized successfully!")

if __name__ == "__main__":
    init_database()
```

---

## ▶️ Run Database Initialization

```bash
python3 init_db.py
```

Expected Output:

```text
Database initialized successfully!
```

---

# 📚 Task 2: Create Database Operations Module

## ✨ Create File

```bash
nano db_operations.py
```

## Add Code

```python
import sqlite3

DATABASE = "library.db"

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def get_all_books():
    conn = get_db_connection()
    books = conn.execute("SELECT * FROM books").fetchall()
    conn.close()

    return [dict(book) for book in books]


def get_book_by_id(book_id):
    conn = get_db_connection()

    book = conn.execute(
        "SELECT * FROM books WHERE id = ?",
        (book_id,)
    ).fetchone()

    conn.close()

    return dict(book) if book else None


def create_book(title, author, year, isbn):
    conn = get_db_connection()

    cursor = conn.execute(
        "INSERT INTO books(title,author,year,isbn) VALUES(?,?,?,?)",
        (title, author, year, isbn)
    )

    conn.commit()

    book_id = cursor.lastrowid

    conn.close()

    return book_id


def update_book(book_id, title, author, year, isbn):
    conn = get_db_connection()

    cursor = conn.execute(
        """
        UPDATE books
        SET title=?, author=?, year=?, isbn=?
        WHERE id=?
        """,
        (title, author, year, isbn, book_id)
    )

    conn.commit()

    updated = cursor.rowcount > 0

    conn.close()

    return updated


def delete_book(book_id):
    conn = get_db_connection()

    cursor = conn.execute(
        "DELETE FROM books WHERE id=?",
        (book_id,)
    )

    conn.commit()

    deleted = cursor.rowcount > 0

    conn.close()

    return deleted
```

---

# 🌐 Task 3: Create Flask REST API

## ✨ Create Application File

```bash
nano app.py
```

---

## Add Code

```python
from flask import Flask, request, jsonify
from flask_cors import CORS
import db_operations

app = Flask(__name__)
CORS(app)


@app.route('/api/books', methods=['GET'])
def get_books():
    books = db_operations.get_all_books()
    return jsonify(books), 200


@app.route('/api/books/<int:book_id>', methods=['GET'])
def get_book(book_id):

    book = db_operations.get_book_by_id(book_id)

    if book:
        return jsonify(book), 200

    return jsonify({"error": "Book not found"}), 404


@app.route('/api/books', methods=['POST'])
def create_book():

    data = request.get_json()

    required = ['title', 'author', 'year', 'isbn']

    if not all(field in data for field in required):
        return jsonify({"error": "Missing required fields"}), 400

    new_id = db_operations.create_book(
        data['title'],
        data['author'],
        data['year'],
        data['isbn']
    )

    return jsonify({
        "id": new_id,
        "message": "Book created"
    }), 201


@app.route('/api/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):

    data = request.get_json()

    updated = db_operations.update_book(
        book_id,
        data['title'],
        data['author'],
        data['year'],
        data['isbn']
    )

    if updated:
        return jsonify({"message": "Book updated"}), 200

    return jsonify({"error": "Book not found"}), 404


@app.route('/api/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):

    deleted = db_operations.delete_book(book_id)

    if deleted:
        return jsonify({"message": "Book deleted"}), 200

    return jsonify({"error": "Book not found"}), 404


@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
```

---

# 🚀 Task 4: Start API Server

Activate virtual environment:

```bash
source ~/rest-api-lab/venv/bin/activate
```

Run Flask:

```bash
python3 app.py
```

Expected Output:

```text
Running on http://0.0.0.0:5000
```

---

# 🧪 API Testing

---

## ❤️ Health Check

```bash
curl http://localhost:5000/api/health
```

Expected:

```json
{
  "status": "healthy"
}
```

---

## 📖 Get All Books

```bash
curl http://localhost:5000/api/books
```

---

## 🔍 Get Book By ID

```bash
curl http://localhost:5000/api/books/1
```

---

## ➕ Create New Book

```bash
curl -X POST http://localhost:5000/api/books \
-H "Content-Type: application/json" \
-d '{
"title":"The Pragmatic Programmer",
"author":"Andrew Hunt",
"year":1999,
"isbn":"9780201616224"
}'
```

Expected:

```json
{
  "id": 4,
  "message": "Book created"
}
```

---

## ✏️ Update Existing Book

```bash
curl -X PUT http://localhost:5000/api/books/1 \
-H "Content-Type: application/json" \
-d '{
"title":"Updated Title",
"author":"Updated Author",
"year":2024,
"isbn":"9781234567890"
}'
```

---

## ❌ Delete Book

```bash
curl -X DELETE http://localhost:5000/api/books/1
```

Expected:

```json
{
  "message": "Book deleted"
}
```

---

## 🔎 Verify Deletion

```bash
curl http://localhost:5000/api/books/1
```

Expected:

```json
{
  "error": "Book not found"
}
```

---

# 🗄️ Verify Database Records

View SQLite data directly:

```bash
sqlite3 library.db "SELECT * FROM books;"
```

---

# ✅ Verification Checklist

| Check | Status |
|---------|---------|
| Database Created | ✅ |
| Flask Running | ✅ |
| GET Endpoint Works | ✅ |
| POST Endpoint Works | ✅ |
| PUT Endpoint Works | ✅ |
| DELETE Endpoint Works | ✅ |
| Health Check Works | ✅ |
| SQLite Data Updated | ✅ |

---

# 🛠️ Troubleshooting

## Issue: Port Already In Use

```bash
sudo lsof -i :5000
kill -9 <PID>
```

---

## Issue: Flask Module Not Found

```bash
source venv/bin/activate

pip install flask flask-cors
```

---

## Issue: Database Locked

### Solution

- Close SQLite sessions
- Restart Flask application

---

## Issue: JSON Decode Error

Verify:

```bash
-H "Content-Type: application/json"
```

Check JSON syntax carefully.

---

## Issue: 404 on All Routes

Verify:

```bash
python3 app.py
```

Ensure application is running.

---

# 🎯 Expected Outcomes

After completing this lab, you should have:

✅ Working Flask REST API

✅ SQLite database integration

✅ CRUD operations

✅ Proper HTTP status codes

✅ JSON request/response handling

✅ API testing experience using curl

---

# 📚 Key Concepts Learned

### REST Architecture

- GET → Retrieve Data
- POST → Create Data
- PUT → Update Data
- DELETE → Remove Data

### Flask

- Route Handling
- JSON Responses
- Request Processing

### SQLite

- Database Creation
- CRUD Operations
- Data Persistence

---

# 🏁 Conclusion

In this lab you successfully:

- Built a RESTful API using Flask
- Connected API endpoints to SQLite
- Implemented full CRUD functionality
- Returned proper HTTP status codes
- Tested APIs using curl
- Managed database records through REST endpoints

These are the foundational skills required for modern backend development, microservices architecture, DevOps automation, and cloud-native application development.

---

# 🚀 Next Steps

- Add Authentication (JWT)
- Implement Input Validation
- Add Pagination
- Create Search Endpoints
- Integrate PostgreSQL
- Deploy API using Docker
- Add Swagger/OpenAPI Documentation
- Write Unit & Integration Tests

---

## 🎉 Completed Successfully

**REST API Development with Flask & SQLite** ✅
