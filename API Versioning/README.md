# 🚀 API Versioning 

<p align="center">

![API](https://img.shields.io/badge/API-Versioning-blue?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.x-yellow?style=for-the-badge\&logo=python)
![Flask](https://img.shields.io/badge/Flask-Web_Framework-black?style=for-the-badge\&logo=flask)
![REST](https://img.shields.io/badge/REST-API-green?style=for-the-badge)
![JSON](https://img.shields.io/badge/JSON-Data_Format-orange?style=for-the-badge\&logo=json)
![Linux](https://img.shields.io/badge/Linux-Ubuntu-red?style=for-the-badge\&logo=linux)

</p>

---

# 📘 API Versioning

## 🎯 Learning Objectives

By the end of this lab, you will be able to:

✅ Implement multiple API versioning strategies

✅ Design versioned routes using URL path versioning

✅ Maintain backward compatibility across API versions

✅ Handle version-specific business logic

✅ Test different API versions simultaneously

---

# 📋 Prerequisites

Before starting this lab, ensure you have:

* Basic understanding of RESTful APIs
* Familiarity with Python and Flask
* Knowledge of HTTP methods (GET, POST, PUT, DELETE)
* Basic Linux command-line skills
* Understanding of JSON format

---

# 🛠️ Environment Setup

## 🔹 Step 1: Update System Packages

```bash
sudo apt update
```

---

## 🔹 Step 2: Install Python and Pip

```bash
sudo apt install python3 python3-pip python3-venv -y
```

---

## 🔹 Step 3: Create Project Directory

```bash
mkdir ~/api-versioning-lab
cd ~/api-versioning-lab
```

---

## 🔹 Step 4: Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 🔹 Step 5: Install Required Packages

```bash
pip install flask requests
```

---

# 🏗️ Task 1: Implement URL Path Versioning

---

## 🔹 Step 1: Create Base Application

```bash
touch app.py
```

Add the following starter code:

```python
from flask import Flask, jsonify, request
from datetime import datetime

app = Flask(__name__)

users_db = {
    1: {"id": 1, "name": "Alice Johnson", "email": "alice@example.com"},
    2: {"id": 2, "name": "Bob Smith", "email": "bob@example.com"}
}
```

---

## 🔹 Step 2: Implement Version 1 Endpoints

### GET All Users (V1)

```python
@app.route('/api/v1/users', methods=['GET'])
def get_users_v1():
    return jsonify(list(users_db.values()))
```

### GET Single User (V1)

```python
@app.route('/api/v1/users/<int:user_id>', methods=['GET'])
def get_user_v1(user_id'):
    user = users_db.get(user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify(user)
```

### 📌 V1 Response Format

```json
{
  "id": 1,
  "name": "Alice Johnson",
  "email": "alice@example.com"
}
```

---

## 🔹 Step 3: Implement Version 2 Endpoints

### GET All Users (V2)

```python
@app.route('/api/v2/users', methods=['GET'])
def get_users_v2():

    users = []

    for user in users_db.values():
        users.append({
            **user,
            "created_at": datetime.now().isoformat(),
            "version": "v2"
        })

    return jsonify(users)
```

---

### GET Single User (V2)

```python
@app.route('/api/v2/users/<int:user_id>', methods=['GET'])
def get_user_v2(user_id):

    user = users_db.get(user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify({
        **user,
        "created_at": datetime.now().isoformat(),
        "version": "v2"
    })
```

---

### POST Create User (V2)

```python
@app.route('/api/v2/users', methods=['POST'])
def create_user_v2():

    data = request.get_json()

    if not data.get("name") or not data.get("email"):
        return jsonify({"error": "Missing required fields"}), 400

    new_id = max(users_db.keys()) + 1

    users_db[new_id] = {
        "id": new_id,
        "name": data["name"],
        "email": data["email"]
    }

    return jsonify({
        **users_db[new_id],
        "created_at": datetime.now().isoformat(),
        "version": "v2"
    }), 201
```

---

## 🔹 Step 4: Start Flask Application

```bash
python3 app.py
```

Expected output:

```text
 * Running on http://0.0.0.0:5000
```

---

# 🧪 Task 2: Test API Version 1

---

## 🔹 Get All Users

```bash
curl http://localhost:5000/api/v1/users
```

---

## 🔹 Get User by ID

```bash
curl http://localhost:5000/api/v1/users/1
```

---

## 🔹 Test Non-Existing User

```bash
curl http://localhost:5000/api/v1/users/999
```

Expected:

```json
{
  "error": "User not found"
}
```

---

# 🧪 Task 3: Test API Version 2

---

## 🔹 Get All Users

```bash
curl http://localhost:5000/api/v2/users
```

---

## 🔹 Get User by ID

```bash
curl http://localhost:5000/api/v2/users/1
```

---

## 🔹 Create User

```bash
curl -X POST http://localhost:5000/api/v2/users \
-H "Content-Type: application/json" \
-d '{
"name":"Charlie Brown",
"email":"charlie@example.com"
}'
```

---

## 🔹 Verify User Creation

```bash
curl http://localhost:5000/api/v2/users/3
```

---

### 📌 V2 Response Format

```json
{
  "id": 1,
  "name": "Alice Johnson",
  "email": "alice@example.com",
  "created_at": "2025-01-15T10:30:00",
  "version": "v2"
}
```

---

# 🔄 Task 4: Implement Version Deprecation

---

## 🔹 Create Utility File

```bash
touch versioning_utils.py
```

Add:

```python
from functools import wraps
from flask import make_response
```

---

### Deprecation Decorator

```python
def deprecated_version(sunset_date):

    def decorator(f):

        @wraps(f)
        def wrapper(*args, **kwargs):

            response = make_response(f(*args, **kwargs))

            response.headers['Sunset'] = sunset_date
            response.headers['Warning'] = '299 - "API v1 is deprecated"'

            return response

        return wrapper

    return decorator
```

---

### Version Response Helper

```python
def version_response(data, version):

    response = make_response(data)

    response.headers['API-Version'] = version

    return response
```

---

## 🔹 Apply Deprecation Decorator

```python
@app.route('/api/v1/users')
@deprecated_version("2025-12-31")
def get_users_v1():
    ...
```

---

# 🧪 Task 5: Verify Deprecation Headers

---

```bash
curl -i http://localhost:5000/api/v1/users
```

Expected headers:

```http
Sunset: 2025-12-31
Warning: 299 - "API v1 is deprecated"
API-Version: v1
```

---

# 🧪 Task 6: Version Comparison Testing

Create:

```bash
touch test_versions.py
```

Example:

```python
import requests

BASE_URL = "http://localhost:5000"

v1 = requests.get(f"{BASE_URL}/api/v1/users/1")
v2 = requests.get(f"{BASE_URL}/api/v2/users/1")

print("V1 Response:")
print(v1.json())

print("\nV2 Response:")
print(v2.json())

print("\nHeaders:")
print(v1.headers)
```

Run:

```bash
python3 test_versions.py
```

---

# ✅ Verification Checklist

## Verify V1

```bash
curl http://localhost:5000/api/v1/users/1
```

Expected:

* ✔ id
* ✔ name
* ✔ email
* ❌ created_at

---

## Verify V2

```bash
curl http://localhost:5000/api/v2/users/1
```

Expected:

* ✔ id
* ✔ name
* ✔ email
* ✔ created_at
* ✔ version

---

## Verify Both Versions Work

```bash
curl http://localhost:5000/api/v1/users
curl http://localhost:5000/api/v2/users
```

Expected:

```text
HTTP 200 OK
```

for both endpoints.

---

# 🛠️ Troubleshooting

## ❌ Import Error

Verify:

```bash
ls
```

Should contain:

```text
app.py
versioning_utils.py
```

---

## ❌ Flask Not Running

Check:

```bash
ps aux | grep python3
```

Restart:

```bash
python3 app.py
```

---

## ❌ JSON Errors

Verify:

```bash
-H "Content-Type: application/json"
```

is included in POST requests.

---

## ❌ Route Not Found

Verify route path:

```text
/api/v1/users
/api/v2/users
```

and not:

```text
/api/users
```

---

# 🎉 Conclusion

Congratulations!

You have successfully:

✅ Implemented API versioning using URL path strategy

✅ Created API v1 and API v2 endpoints

✅ Added version-specific functionality

✅ Maintained backward compatibility

✅ Implemented API deprecation warnings

✅ Tested multiple API versions simultaneously

---

# 📚 Key Takeaways

* API versioning prevents breaking existing clients.
* URL path versioning is simple and widely adopted.
* Backward compatibility is critical in production systems.
* Deprecation headers help clients migrate safely.
* Multiple API versions can coexist during transitions.

---

# 🚀 Next Steps

Explore:

* Header-based API versioning
* Query parameter versioning
* Content negotiation versioning
* OpenAPI/Swagger documentation
* API Gateway version management
* Microservices API lifecycle management

---

## 🧹 Cleanup

Deactivate virtual environment:

```bash
deactivate
```

Remove lab directory:

```bash
rm -rf ~/api-versioning-lab
```

---

⭐ **Lab Completed Successfully!**
