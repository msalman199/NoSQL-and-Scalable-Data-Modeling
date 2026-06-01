# 📚 Swagger/OpenAPI Documentation 

![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge\&logo=python)
![Flask](https://img.shields.io/badge/Flask-Web_Framework-black?style=for-the-badge\&logo=flask)
![Swagger](https://img.shields.io/badge/Swagger-OpenAPI-green?style=for-the-badge\&logo=swagger)
![REST API](https://img.shields.io/badge/REST-API-orange?style=for-the-badge)
![Linux](https://img.shields.io/badge/Linux-Ubuntu-E95420?style=for-the-badge\&logo=ubuntu)

---

# 🚀 Swagger/OpenAPI Documentation

## 📖 Overview

Swagger/OpenAPI is an industry-standard specification for designing, documenting, and testing RESTful APIs. It provides interactive API documentation that allows developers to explore and test endpoints directly from a web browser.

In this lab, you will build a Flask REST API and automatically generate interactive Swagger UI documentation using **Flask-RESTX**.

---

# 🎯 Learning Objectives

By the end of this lab, you will be able to:

✅ Implement OpenAPI 3.0 specification in a Flask application

✅ Generate interactive Swagger UI documentation automatically

✅ Customize API documentation with descriptions, examples, and schemas

✅ Test API endpoints directly through Swagger UI

✅ Validate API requests and responses against OpenAPI schemas

---

# 📋 Prerequisites

Before starting this lab, ensure you have:

* Basic understanding of REST APIs
* Familiarity with Python and Flask
* Knowledge of JSON structures
* Basic Linux command-line skills
* Understanding of API request/response patterns

---

# 🛠️ Environment Setup

## 🔄 Update Package Manager

```bash
sudo apt update
```

---

## 📦 Install Python and Pip

```bash
sudo apt install -y python3 python3-pip python3-venv
```

---

## 📁 Create Project Directory

```bash
mkdir ~/swagger-lab
cd ~/swagger-lab
```

---

## 🐍 Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 📥 Install Required Packages

```bash
pip install flask flask-restx werkzeug==2.3.0
```

> Flask-RESTX provides built-in Swagger/OpenAPI integration.

---

# 🏗️ Task 1: Create Basic API with Swagger Documentation

---

## ✨ Step 1: Create Application File

```bash
nano app.py
```

### Add Base Application

```python
from flask import Flask, request
from flask_restx import Api, Resource, fields
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)

api = Api(
    app,
    version='1.0',
    title='Book Library API',
    description='A simple API for managing a book library',
    doc='/docs'
)

ns = api.namespace('books', description='Book operations')

books_db = [
    {'id': 1, 'title': '1984', 'author': 'George Orwell', 'year': 1949},
    {'id': 2, 'title': 'To Kill a Mockingbird', 'author': 'Harper Lee', 'year': 1960}
]

book_model = api.model('Book', {
    'id': fields.Integer(required=True, description='Book ID'),
    'title': fields.String(required=True, description='Book title'),
    'author': fields.String(required=True, description='Book author'),
    'year': fields.Integer(required=True, description='Publication year')
})

book_input_model = api.model('BookInput', {
    'title': fields.String(required=True),
    'author': fields.String(required=True),
    'year': fields.Integer(required=True)
})
```

---

## 📚 Step 2: Implement CRUD Endpoints

### GET and POST Operations

```python
@ns.route('/')
class BookList(Resource):

    @ns.doc('list_books')
    @ns.marshal_list_with(book_model)
    def get(self):
        return books_db

    @ns.doc('create_book')
    @ns.expect(book_input_model)
    @ns.marshal_with(book_model, code=201)
    def post(self):
        data = api.payload

        new_book = {
            'id': max([b['id'] for b in books_db]) + 1,
            'title': data['title'],
            'author': data['author'],
            'year': data['year']
        }

        books_db.append(new_book)

        return new_book, 201
```

---

### GET, PUT and DELETE by ID

```python
@ns.route('/<int:id>')
@ns.response(404, 'Book not found')
@ns.param('id', 'Book ID')
class Book(Resource):

    @ns.marshal_with(book_model)
    def get(self, id):
        for book in books_db:
            if book['id'] == id:
                return book

        api.abort(404, "Book not found")

    def delete(self, id):
        for i, book in enumerate(books_db):
            if book['id'] == id:
                books_db.pop(i)
                return '', 204

        api.abort(404, "Book not found")

    @ns.expect(book_input_model)
    @ns.marshal_with(book_model)
    def put(self, id):
        for book in books_db:
            if book['id'] == id:
                book.update(api.payload)
                return book

        api.abort(404, "Book not found")
```

---

## ▶️ Step 3: Run Application

```bash
python3 app.py
```

---

## 🌐 Access Swagger UI

Open your browser:

```text
http://localhost:5000/docs
```

You should see an interactive Swagger UI dashboard.

---

# 🚀 Task 2: Enhance API Documentation

---

## 📝 Advanced API Configuration

```python
api = Api(
    app,
    version='2.0',
    title='Book Library API',
    description='Advanced Book Management API',
    doc='/docs',
    contact='admin@library.com',
    license='MIT'
)
```

---

## 📘 Enhanced Book Model

```python
book_model = api.model('Book', {
    'id': fields.Integer(readonly=True),
    'title': fields.String(required=True,
                           example='The Great Gatsby'),
    'author': fields.String(required=True,
                            example='F. Scott Fitzgerald'),
    'year': fields.Integer(required=True,
                           example=1925),
    'isbn': fields.String(
        example='978-0743273565'
    )
})
```

---

## 🔍 Add Query Parameter Filtering

### Create Parser

```python
search_parser = reqparse.RequestParser()

search_parser.add_argument(
    'author',
    type=str,
    help='Filter by author',
    location='args'
)

search_parser.add_argument(
    'year',
    type=int,
    help='Filter by publication year',
    location='args'
)
```

---

### Implement Filtering Logic

```python
args = search_parser.parse_args()

result = books_db

if args['author']:
    result = [
        b for b in result
        if args['author'].lower()
        in b['author'].lower()
    ]

if args['year']:
    result = [
        b for b in result
        if b['year'] == args['year']
    ]

return result
```

---

# 🧪 Testing the API

---

## 📖 List All Books

```bash
curl -X GET http://localhost:5000/books/
```

---

## ➕ Create Book

```bash
curl -X POST http://localhost:5000/books/ \
-H "Content-Type: application/json" \
-d '{
"title":"Brave New World",
"author":"Aldous Huxley",
"year":1932,
"isbn":"978-0060850524"
}'
```

---

## 🔍 Get Book by ID

```bash
curl -X GET http://localhost:5000/books/1
```

---

## 🔎 Search by Author

```bash
curl -X GET \
"http://localhost:5000/books/?author=Orwell"
```

---

## ✏️ Update Book

```bash
curl -X PUT http://localhost:5000/books/1 \
-H "Content-Type: application/json" \
-d '{
"title":"1984 (Updated)",
"author":"George Orwell",
"year":1949,
"isbn":"978-0451524935"
}'
```

---

## ❌ Delete Book

```bash
curl -X DELETE \
http://localhost:5000/books/2
```

---

# ✅ Verification

---

## Verify Swagger UI

```bash
curl http://localhost:5000/docs
```

Expected:

```text
Swagger UI HTML page
```

---

## Verify OpenAPI Specification

Download API schema:

```bash
curl http://localhost:5000/swagger.json \
-o openapi_spec.json
```

Pretty print:

```bash
cat openapi_spec.json | python3 -m json.tool
```

Expected:

* OpenAPI JSON document
* Paths
* Definitions
* Models
* Schemas

---

# 🔧 Troubleshooting

---

## ⚠️ Swagger UI Not Loading

Check running process:

```bash
sudo netstat -tlnp | grep 5000
```

Kill existing process:

```bash
sudo kill -9 <PID>
```

---

## ⚠️ Flask-RESTX Import Error

Activate environment:

```bash
source ~/swagger-lab/venv/bin/activate
```

Reinstall packages:

```bash
pip install flask flask-restx werkzeug==2.3.0
```

---

## ⚠️ Validation Not Working

Ensure:

```python
@ns.expect(book_input_model, validate=True)
```

is used.

---

## ⚠️ Models Missing in Swagger UI

Verify:

```python
@ns.marshal_with()
@ns.expect()
```

are properly applied.

---

# 📊 Expected Outcomes

After completing this lab you should have:

✅ Interactive Swagger UI documentation

✅ OpenAPI-compliant API specification

✅ Request and response validation

✅ Search and filtering functionality

✅ Self-documenting REST API

✅ API schemas and examples

---

# 🎓 Conclusion

Congratulations! 🎉

You have successfully:

* Built a Flask REST API
* Generated automatic Swagger/OpenAPI documentation
* Created request and response schemas
* Added validation and examples
* Implemented filtering and search functionality
* Tested APIs through Swagger UI and curl

---

## 💡 Key Takeaways

✔ OpenAPI provides standardized API documentation

✔ Swagger UI enables interactive API testing

✔ Well-documented APIs improve developer productivity

✔ Validation reduces API misuse

✔ Flask-RESTX simplifies documentation generation

---

# 🚀 Next Steps

Explore the following advanced topics:

* API Key Authentication Documentation
* JWT Authentication Documentation
* OAuth2 Integration
* API Versioning
* Response Examples
* Client SDK Generation
* OpenAPI 3.1 Features
* Microservice API Documentation

---

# 🧹 Cleanup (Optional)

```bash
deactivate

cd ~

rm -rf ~/swagger-lab
```

---

## 🎯 Lab Completed Successfully

**Swagger/OpenAPI Documentation with Flask RESTX**
