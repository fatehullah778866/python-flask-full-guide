# Lesson 5.5: API Documentation - Helping Others Use Your API! 📚

## What is API Documentation? 📖

**API Documentation** = Instructions on how to use your API

Think of it like:
- **User Manual** = How to use a product
- **API Documentation** = How to use an API

**Good documentation = Easy to use API!**

## Why Do We Need Documentation? 🎯

### Without Documentation:

- ❌ Users don't know what endpoints exist
- ❌ Users don't know what data to send
- ❌ Users don't know what to expect back
- ❌ Users get frustrated and give up

### With Documentation:

- ✅ Users know all endpoints
- ✅ Users know what data to send
- ✅ Users know what to expect
- ✅ Users can use your API easily!

## Types of Documentation 📋

### 1. Simple Text Documentation

**Like**: A README file

```markdown
# User API

## GET /api/users
Returns all users

Response:
{
  "users": [...]
}
```

### 2. Interactive Documentation (Swagger/OpenAPI)

**Like**: A website where you can test the API

- See all endpoints
- Try them out
- See examples

## Creating Simple Documentation 📝

### Method 1: README File

```markdown
# User API Documentation

## Base URL
http://localhost:5000/api

## Endpoints

### GET /users
Get all users

**Response:**
```json
{
  "users": [
    {"id": 1, "name": "John", "email": "john@email.com"}
  ]
}
```

### POST /users
Create a new user

**Request Body:**
```json
{
  "name": "John",
  "email": "john@email.com"
}
```

**Response:**
```json
{
  "id": 1,
  "name": "John",
  "email": "john@email.com"
}
```
```

## Using Flask-Swagger/OpenAPI 🚀

### Installing Flask-Swagger

```bash
pip install flask-swagger-ui
```

### Setting Up Swagger

```python
from flask import Flask
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)

# Swagger configuration
SWAGGER_URL = '/api/docs'
API_URL = '/api/swagger.json'

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "User API"
    }
)

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)
```

### Creating Swagger JSON

```python
@app.route('/api/swagger.json')
def swagger():
    return jsonify({
        "swagger": "2.0",
        "info": {
            "title": "User API",
            "version": "1.0.0",
            "description": "API for managing users"
        },
        "paths": {
            "/api/users": {
                "get": {
                    "summary": "Get all users",
                    "responses": {
                        "200": {
                            "description": "List of users"
                        }
                    }
                },
                "post": {
                    "summary": "Create a user",
                    "parameters": [
                        {
                            "name": "body",
                            "in": "body",
                            "required": True,
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "name": {"type": "string"},
                                    "email": {"type": "string"}
                                }
                            }
                        }
                    ],
                    "responses": {
                        "201": {
                            "description": "User created"
                        }
                    }
                }
            }
        }
    })
```

## Using Flask-RESTX (Better Swagger) 🎁

### Installing Flask-RESTX

```bash
pip install flask-restx
```

### Setting Up Flask-RESTX

```python
from flask import Flask
from flask_restx import Api, Resource, fields

app = Flask(__name__)
api = Api(
    app,
    version='1.0',
    title='User API',
    description='API for managing users',
    doc='/api/docs/'
)

# Define models
user_model = api.model('User', {
    'id': fields.Integer(readonly=True, description='User ID'),
    'name': fields.String(required=True, description='User name'),
    'email': fields.String(required=True, description='User email')
})

# Resource with documentation
@api.route('/users')
class UserList(Resource):
    @api.doc('list_users')
    @api.marshal_list_with(user_model)
    def get(self):
        """Get all users"""
        users = User.query.all()
        return [user.to_dict() for user in users]
    
    @api.doc('create_user')
    @api.expect(user_model)
    @api.marshal_with(user_model, code=201)
    def post(self):
        """Create a new user"""
        data = api.payload
        user = User(name=data['name'], email=data['email'])
        db.session.add(user)
        db.session.commit()
        return user.to_dict(), 201

if __name__ == '__main__':
    app.run(debug=True)
```

## Documenting with Comments 📝

### Method 1: Docstrings

```python
class UserListResource(Resource):
    def get(self):
        """
        Get all users
        
        Returns a list of all users in the system.
        
        Returns:
            dict: JSON response with list of users
        """
        users = User.query.all()
        return {"users": [user.to_dict() for user in users]}
```

### Method 2: Inline Comments

```python
@app.route('/api/users', methods=['GET'])
def get_users():
    """
    GET /api/users
    
    Returns all users.
    
    Response:
        200 OK - List of users
    """
    users = User.query.all()
    return jsonify({"users": [user.to_dict() for user in users]})
```

## Best Practices for Documentation ✨

### 1. Document All Endpoints

✅ **Good**: Every endpoint has documentation
❌ **Bad**: Some endpoints missing documentation

### 2. Include Examples

✅ **Good**: Shows example requests and responses
❌ **Bad**: Only describes what it does

### 3. Document Parameters

✅ **Good**: Lists all parameters and what they do
❌ **Bad**: Doesn't explain parameters

### 4. Document Errors

✅ **Good**: Lists possible error responses
❌ **Bad**: Doesn't mention errors

### 5. Keep It Updated

✅ **Good**: Documentation matches code
❌ **Bad**: Documentation is outdated

## Simple Documentation Template 📄

```markdown
# API Documentation

## Base URL
`http://localhost:5000/api`

## Authentication
Include token in header:
```
Authorization: Bearer your-token-here
```

## Endpoints

### GET /users
Get all users

**Response:**
- Status: 200 OK
- Body:
```json
{
  "users": [
    {
      "id": 1,
      "name": "John",
      "email": "john@email.com"
    }
  ]
}
```

### POST /users
Create a new user

**Request:**
- Body:
```json
{
  "name": "John",
  "email": "john@email.com"
}
```

**Response:**
- Status: 201 Created
- Body:
```json
{
  "id": 1,
  "name": "John",
  "email": "john@email.com"
}
```

**Errors:**
- 400 Bad Request - Invalid data
- 400 Bad Request - Email already exists
```

## Testing Your Documentation 🧪

### Use Postman or Insomnia

1. **Import your API**
2. **Test each endpoint**
3. **Verify documentation matches**

### Create Test Examples

```python
# Example test
def test_get_users():
    response = client.get('/api/users')
    assert response.status_code == 200
    assert 'users' in response.json
```

## What You Learned! 📚

✅ Why API documentation is important  
✅ Types of documentation  
✅ How to create simple documentation  
✅ How to use Flask-Swagger  
✅ How to use Flask-RESTX  
✅ Best practices for documentation  

## Key Concepts 💡

1. **Documentation** = Instructions for using API
2. **Swagger/OpenAPI** = Interactive documentation
3. **Flask-RESTX** = Tool for API documentation
4. **Examples** = Show how to use API
5. **Keep Updated** = Documentation should match code

## What's Next? 🚀

Congratulations! You've completed Module 5! You now know:
- ✅ What APIs are
- ✅ How to build REST APIs
- ✅ How to use Flask-RESTful
- ✅ How to authenticate APIs
- ✅ How to document APIs

**Next Module**: Advanced Flask Features - Learn blueprints, application factories, and more!

---

**Amazing! You're now an API expert! 🎉**

