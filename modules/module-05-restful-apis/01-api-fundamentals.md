# Lesson 5.1: API Fundamentals - What is an API? 🌐

## What is an API? 🤔

**API** = Application Programming Interface

Think of an API like a **waiter in a restaurant**:

- **You (the customer)** = Want food
- **Waiter (the API)** = Takes your order, brings it to kitchen, brings food back
- **Kitchen (the server)** = Makes the food
- **Food (the data)** = What you get back

**API = A way for different programs to talk to each other!**

## Real-World Example 🌍

### Without API:

Imagine you want to see weather on your phone:
- ❌ Your phone would need to have its own weather station
- ❌ Every phone would need weather equipment
- ❌ Impossible!

### With API:

- ✅ Your phone asks a weather API: "What's the weather?"
- ✅ Weather API responds: "It's sunny, 75°F"
- ✅ Your phone shows you the weather!

**APIs let apps share information!**

## What is REST? 🛣️

**REST** = Representational State Transfer

Think of REST like **rules for how to talk**:

- **Like speaking a language** - Everyone follows the same rules
- **Makes communication easy** - Everyone understands each other
- **Standard way** - Works the same everywhere

### REST is Like:

- **HTTP** = The language (how to communicate)
- **REST** = The grammar rules (how to structure communication)

## Understanding HTTP Methods 📡

HTTP methods are like **different types of requests**:

### 1. GET - "Give me information" 📖

**Like**: Asking a question

```
GET /users
→ "Show me all users"
→ Returns: List of users
```

**Use for**: Reading data (getting information)

### 2. POST - "Here's new information" ➕

**Like**: Submitting a form

```
POST /users
→ "Create a new user with this data"
→ Returns: The created user
```

**Use for**: Creating new data

### 3. PUT - "Update this information" ✏️

**Like**: Editing a document

```
PUT /users/1
→ "Update user #1 with this data"
→ Returns: Updated user
```

**Use for**: Updating existing data

### 4. DELETE - "Remove this information" 🗑️

**Like**: Throwing something away

```
DELETE /users/1
→ "Delete user #1"
→ Returns: Success message
```

**Use for**: Deleting data

### 5. PATCH - "Partially update" 🔧

**Like**: Changing just one thing

```
PATCH /users/1
→ "Change only the email for user #1"
→ Returns: Updated user
```

**Use for**: Partial updates

## RESTful Principles 📋

### Principle 1: Use Nouns, Not Verbs

❌ **Bad**:
```
/getUsers
/createUser
/deleteUser
```

✅ **Good**:
```
GET /users
POST /users
DELETE /users/1
```

### Principle 2: Use HTTP Methods

❌ **Bad**:
```
/users/get
/users/create
```

✅ **Good**:
```
GET /users
POST /users
```

### Principle 3: Use Plural Nouns

❌ **Bad**:
```
/user
/book
```

✅ **Good**:
```
/users
/books
```

### Principle 4: Use Status Codes

✅ **Good**:
```
200 OK - Success
201 Created - Resource created
404 Not Found - Resource doesn't exist
400 Bad Request - Invalid request
```

## Understanding URLs (Endpoints) 🔗

### What is an Endpoint?

An **endpoint** is like an **address** for your API:

```
https://api.example.com/users
```

- **`https://`** = Protocol (how to communicate)
- **`api.example.com`** = Server address
- **`/users`** = Endpoint (what you want)

### Endpoint Examples:

```
GET    /users           → Get all users
GET    /users/1         → Get user with ID 1
POST   /users           → Create a new user
PUT    /users/1         → Update user with ID 1
DELETE /users/1         → Delete user with ID 1
```

## Understanding JSON 📄

### What is JSON?

**JSON** = JavaScript Object Notation

It's like a **universal language** for data:

```json
{
  "name": "John",
  "age": 25,
  "email": "john@email.com"
}
```

### JSON Structure:

- **`{}`** = Object (like a dictionary)
- **`[]`** = Array (like a list)
- **`"key": "value"`** = Key-value pairs
- **Strings** = Always in quotes
- **Numbers** = No quotes

### JSON Example:

```json
{
  "users": [
    {
      "id": 1,
      "name": "John",
      "email": "john@email.com"
    },
    {
      "id": 2,
      "name": "Sarah",
      "email": "sarah@email.com"
    }
  ]
}
```

## HTTP Status Codes 📊

Status codes tell you **what happened**:

### Success Codes (2xx):

- **200 OK** = Request successful
- **201 Created** = Resource created successfully
- **204 No Content** = Success, but no content to return

### Client Error Codes (4xx):

- **400 Bad Request** = Invalid request
- **401 Unauthorized** = Not authenticated
- **403 Forbidden** = Not allowed
- **404 Not Found** = Resource doesn't exist
- **422 Unprocessable Entity** = Valid format, but can't process

### Server Error Codes (5xx):

- **500 Internal Server Error** = Server error
- **503 Service Unavailable** = Service down

## API Request and Response 🔄

### Request (What You Send):

```
GET /users/1 HTTP/1.1
Host: api.example.com
```

**Breaking it down:**
- **Method**: GET
- **Path**: /users/1
- **Host**: Where to send it

### Response (What You Get Back):

```
HTTP/1.1 200 OK
Content-Type: application/json

{
  "id": 1,
  "name": "John",
  "email": "john@email.com"
}
```

**Breaking it down:**
- **Status**: 200 OK
- **Content-Type**: JSON
- **Body**: The data

## RESTful API Design Best Practices ✨

### 1. Use Clear, Consistent URLs

✅ **Good**:
```
GET    /api/v1/users
POST   /api/v1/users
GET    /api/v1/users/1
PUT    /api/v1/users/1
DELETE /api/v1/users/1
```

### 2. Use Proper HTTP Methods

✅ **Good**:
- GET for reading
- POST for creating
- PUT for updating
- DELETE for deleting

### 3. Return Proper Status Codes

✅ **Good**:
- 200 for success
- 201 for created
- 404 for not found
- 400 for bad request

### 4. Use JSON Format

✅ **Good**:
```json
{
  "id": 1,
  "name": "John"
}
```

### 5. Version Your API

✅ **Good**:
```
/api/v1/users
/api/v2/users
```

## Real-World API Examples 🌐

### Example 1: Weather API

```
GET https://api.weather.com/current?city=NewYork
→ Returns: {"temperature": 75, "condition": "sunny"}
```

### Example 2: Social Media API

```
GET https://api.twitter.com/users/123/posts
→ Returns: List of posts
```

### Example 3: E-Commerce API

```
GET https://api.shop.com/products
→ Returns: List of products
```

## Why Use APIs? 🎯

### Benefits:

1. **Reusability** - One API, many apps can use it
2. **Separation** - Frontend and backend can be separate
3. **Scalability** - Easy to scale
4. **Integration** - Different systems can work together
5. **Mobile Apps** - Mobile apps can use same API

## API vs Website 🌐

### Website:

- Returns **HTML** (web pages)
- For **humans** to read
- Shows in **browser**

### API:

- Returns **JSON** (data)
- For **programs** to read
- Used by **apps**

**Same backend, different output!**

## Practice Exercise 🏋️

Design API endpoints for a blog:

1. **Get all posts**: `GET /posts`
2. **Get one post**: `GET /posts/1`
3. **Create post**: `POST /posts`
4. **Update post**: `PUT /posts/1`
5. **Delete post**: `DELETE /posts/1`

**What HTTP methods would you use for each?**

## What You Learned! 📚

✅ What APIs are and why we need them  
✅ What REST is  
✅ HTTP methods (GET, POST, PUT, DELETE)  
✅ RESTful principles  
✅ Understanding URLs and endpoints  
✅ What JSON is  
✅ HTTP status codes  
✅ API design best practices  

## Key Concepts 💡

1. **API** = Way for programs to communicate
2. **REST** = Rules for building APIs
3. **HTTP Methods** = GET, POST, PUT, DELETE
4. **Endpoint** = URL path for API
5. **JSON** = Data format for APIs
6. **Status Codes** = Tell you what happened

## What's Next? 🚀

Now that you understand APIs, let's learn how to **build REST APIs with Flask**!

---

**Great job! You now understand the basics of APIs! 🎉**

