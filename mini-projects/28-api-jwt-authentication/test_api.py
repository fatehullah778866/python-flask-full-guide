# Test Script for JWT API
# This script demonstrates how to use the JWT API

# Step 1: Import Requests Library
# What is this? Importing library for making HTTP requests
import requests
# Explanation:
# - requests = Library for making HTTP requests
# - We'll use this to test the API
# - Install with: pip install requests

# Step 2: Set Base URL
# What is this? The base URL for the API
BASE_URL = 'http://127.0.0.1:5000'
# Explanation:
# - BASE_URL = Base URL for API
# - 'http://127.0.0.1:5000' = Local Flask server
# - We'll append endpoint paths to this

# Step 3: Test Registration
# What is this? Testing user registration
print("=== Testing Registration ===")
# Explanation:
# - print() = Displays text in console
# - Shows what test we're running

register_data = {
    'username': 'testuser',
    'email': 'test@example.com',
    'password': 'testpass123'
}
# Explanation:
# - register_data = Dictionary with registration data
# - username, email, password = User information

response = requests.post(f'{BASE_URL}/api/register', json=register_data)
# Explanation:
# - requests.post() = Makes POST request
# - f'{BASE_URL}/api/register' = Full URL for registration endpoint
# - json=register_data = Sends data as JSON
# - response = Response object from server

print(f"Status Code: {response.status_code}")
# Explanation:
# - response.status_code = HTTP status code
# - 201 = Created (success)
# - 400 = Bad Request (error)

print(f"Response: {response.json()}")
# Explanation:
# - response.json() = Converts response to dictionary
# - Shows the JSON response from server
# - Example: {'message': 'User registered successfully', ...}

print()

# Step 4: Test Login
# What is this? Testing user login
print("=== Testing Login ===")

login_data = {
    'username': 'testuser',
    'password': 'testpass123'
}
# Explanation:
# - login_data = Dictionary with login data
# - username, password = User credentials

response = requests.post(f'{BASE_URL}/api/login', json=login_data)
# Explanation:
# - requests.post() = Makes POST request
# - f'{BASE_URL}/api/login' = Full URL for login endpoint
# - json=login_data = Sends data as JSON
# - response = Response object from server

print(f"Status Code: {response.status_code}")
print(f"Response: {response.json()}")

# Step 5: Extract Tokens
# What is this? Getting tokens from login response
response_data = response.json()
# Explanation:
# - response.json() = Converts response to dictionary
# - response_data = Dictionary with tokens and user info

access_token = response_data.get('access_token')
refresh_token = response_data.get('refresh_token')
# Explanation:
# - response_data.get('access_token') = Gets access token
# - response_data.get('refresh_token') = Gets refresh token
# - access_token = JWT access token
# - refresh_token = JWT refresh token

print(f"Access Token: {access_token[:50]}...")
# Explanation:
# - access_token[:50] = First 50 characters of token
# - Shows part of token (tokens are long!)
# - ... = Indicates there's more

print()

# Step 6: Test Protected Endpoint
# What is this? Testing endpoint that requires authentication
print("=== Testing Protected Endpoint (Get Resources) ===")

headers = {
    'Authorization': f'Bearer {access_token}'
}
# Explanation:
# - headers = Dictionary with HTTP headers
# - 'Authorization' = Header name for authentication
# - f'Bearer {access_token}' = Authorization header value
# - Bearer = Token type (standard for JWT)
# - access_token = The JWT token from login

response = requests.get(f'{BASE_URL}/api/resources', headers=headers)
# Explanation:
# - requests.get() = Makes GET request
# - f'{BASE_URL}/api/resources' = Full URL for resources endpoint
# - headers=headers = Sends authorization header
# - response = Response object from server

print(f"Status Code: {response.status_code}")
print(f"Response: {response.json()}")
print()

# Step 7: Test Create Resource
# What is this? Testing creating a resource
print("=== Testing Create Resource ===")

resource_data = {
    'name': 'Test Resource',
    'description': 'This is a test resource'
}
# Explanation:
# - resource_data = Dictionary with resource data
# - name, description = Resource information

response = requests.post(f'{BASE_URL}/api/resources', json=resource_data, headers=headers)
# Explanation:
# - requests.post() = Makes POST request
# - f'{BASE_URL}/api/resources' = Full URL for create resource endpoint
# - json=resource_data = Sends data as JSON
# - headers=headers = Sends authorization header
# - response = Response object from server

print(f"Status Code: {response.status_code}")
print(f"Response: {response.json()}")
print()

# Step 8: Test Token Refresh
# What is this? Testing token refresh
print("=== Testing Token Refresh ===")

refresh_headers = {
    'Authorization': f'Bearer {refresh_token}'
}
# Explanation:
# - refresh_headers = Dictionary with HTTP headers
# - 'Authorization' = Header name
# - f'Bearer {refresh_token}' = Authorization header with refresh token
# - Uses refresh token instead of access token

response = requests.post(f'{BASE_URL}/api/refresh', headers=refresh_headers)
# Explanation:
# - requests.post() = Makes POST request
# - f'{BASE_URL}/api/refresh' = Full URL for refresh endpoint
# - headers=refresh_headers = Sends refresh token in header
# - response = Response object from server

print(f"Status Code: {response.status_code}")
print(f"Response: {response.json()}")

new_access_token = response.json().get('access_token')
# Explanation:
# - response.json() = Converts response to dictionary
# - .get('access_token') = Gets new access token
# - new_access_token = New JWT access token
# - This is a fresh token (valid for 1 hour)

print(f"New Access Token: {new_access_token[:50]}...")
# Explanation:
# - Shows part of new token
# - This token can be used for API requests

print()
print("=== All Tests Complete ===")
# Explanation:
# - Shows that all tests finished
# - This script demonstrates the full API workflow!

