from flask import Flask, jsonify, request
from datetime import datetime

app = Flask(__name__)

# Sample data store
users_db = {
    1: {"id": 1, "name": "Alice Johnson", "email": "alice@example.com"},
    2: {"id": 2, "name": "Bob Smith", "email": "bob@example.com"}
}

# TODO: Implement v1 API endpoints
# Version 1: Basic user information (name and email only)

@app.route('/api/v1/users', methods=['GET'])
def get_users_v1():
    """
    Return all users with basic information (v1 format).
    Should return: id, name, email
    """
    # TODO: Implement logic to return users in v1 format
    pass

@app.route('/api/v1/users/<int:user_id>', methods=['GET'])
def get_user_v1(user_id):
    """
    Return single user with basic information (v1 format).
    
    Args:
        user_id: Integer ID of the user
    """
    # TODO: Implement logic to return single user
    # TODO: Handle user not found case
    pass

# TODO: Implement v2 API endpoints
# Version 2: Enhanced user information with metadata

@app.route('/api/v2/users', methods=['GET'])
def get_users_v2():
    """
    Return all users with enhanced information (v2 format).
    Should return: id, name, email, created_at, version
    """
    # TODO: Implement logic to return users in v2 format
    # TODO: Add metadata fields (created_at, version)
    pass

@app.route('/api/v2/users/<int:user_id>', methods=['GET'])
def get_user_v2(user_id):
    """
    Return single user with enhanced information (v2 format).
    
    Args:
        user_id: Integer ID of the user
    """
    # TODO: Implement logic to return single user with metadata
    # TODO: Handle user not found case
    pass

# TODO: Implement POST endpoint for v2 only
@app.route('/api/v2/users', methods=['POST'])
def create_user_v2():
    """
    Create new user (v2 only feature).
    Expected JSON: {"name": "string", "email": "string"}
    """
    # TODO: Get JSON data from request
    # TODO: Validate required fields
    # TODO: Generate new user ID
    # TODO: Add user to database with metadata
    # TODO: Return created user
    pass

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
