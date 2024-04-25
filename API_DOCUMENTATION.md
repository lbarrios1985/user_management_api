# User Management API Documentation

## Overview
A RESTful API for user management, built with FastAPI and SQLAlchemy. Supports CRUD operations, robust validation, logging, and is ready for cloud deployment.

---

## API Endpoints

### 1. Create User
- **POST** `/users/`
- **Description:** Create a new user. Username and email must be unique.
- **Request Body:**
  ```json
  {
    "username": "jdoe",
    "email": "jdoe@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "role": "user",
    "active": true
  }
  ```
- **Success Response:** `201 Created`
  ```json
  {
    "id": 1,
    "username": "jdoe",
    "email": "jdoe@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "role": "user",
    "active": true,
    "created_at": "2025-04-29T12:00:00",
    "updated_at": "2025-04-29T12:00:00"
  }
  ```
- **Error Responses:**
  - `400 Bad Request`: Username or email already exists, or validation error.

---

### 2. List Users
- **GET** `/users/`
- **Description:** List all users (supports pagination with `skip` and `limit` query params).
- **Success Response:** `200 OK`
  ```json
  [
    {
      "id": 1,
      "username": "jdoe",
      "email": "jdoe@example.com",
      ...
    },
    ...
  ]
  ```

---

### 3. Get User by ID
- **GET** `/users/{user_id}`
- **Description:** Retrieve a user by their unique ID.
- **Success Response:** `200 OK`
  ```json
  {
    "id": 1,
    "username": "jdoe",
    ...
  }
  ```
- **Error Response:** `404 Not Found`: User not found.

---

### 4. Update User
- **PUT** `/users/{user_id}`
- **Description:** Update user fields. Only provided fields will be updated.
- **Request Body Example:**
  ```json
  {
    "first_name": "Jane",
    "active": false
  }
  ```
- **Success Response:** `200 OK` (returns updated user)
- **Error Response:** `404 Not Found`: User not found.

---

### 5. Delete User
- **DELETE** `/users/{user_id}`
- **Description:** Delete a user by their unique ID.
- **Success Response:** `200 OK`
  ```json
  { "detail": "User deleted." }
  ```
- **Error Response:** `404 Not Found`: User not found.

---

## OpenAPI/Swagger Documentation
- **Interactive Docs:** Visit `/docs` (Swagger UI) or `/redoc` (ReDoc) when running the server.
- **All endpoints** are documented with summaries, descriptions, request/response schemas, and example values.

---

## Validation & Error Handling
- **Input Validation:** All fields are validated using Pydantic:
  - `username`, `first_name`, `last_name`: required, min/max length, no whitespace.
  - `email`: must be a valid email.
  - `role`: must be one of `admin`, `user`, or `guest`.
  - `active`: boolean.
- **Unique Constraints:** Username and email must be unique. Attempts to create duplicates return `400 Bad Request`.
- **Not Found:** Accessing, updating, or deleting a non-existent user returns `404 Not Found`.
- **Database Errors:** Integrity errors are caught and return a descriptive HTTP error.
- **Logging:** All CRUD operations log the action and relevant identifiers.

---

## Example Error Responses
- **Duplicate User:**
  ```json
  {
    "detail": "Username or email already exists."
  }
  ```
- **User Not Found:**
  ```json
  {
    "detail": "User not found."
  }
  ```
- **Validation Error:**
  ```json
  {
    "detail": [
      {
        "loc": ["body", "email"],
        "msg": "value is not a valid email address",
        "type": "value_error.email"
      }
    ]
  }
  ```

---

## Example API Calls (curl)

### Create User
```bash
curl -X POST http://localhost:8000/users/ \
  -H 'Content-Type: application/json' \
  -d '{
    "username": "jdoe",
    "email": "jdoe@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "role": "user",
    "active": true
  }'
```

### List Users
```bash
curl http://localhost:8000/users/
```

### Get User by ID
```bash
curl http://localhost:8000/users/1
```

### Update User
```bash
curl -X PUT http://localhost:8000/users/1 \
  -H 'Content-Type: application/json' \
  -d '{ "first_name": "Jane" }'
```

### Delete User
```bash
curl -X DELETE http://localhost:8000/users/1
```

---

## Postman Collection

1. Import the following endpoints into Postman:
   - POST /users/
   - GET /users/
   - GET /users/{user_id}
   - PUT /users/{user_id}
   - DELETE /users/{user_id}
2. Set Content-Type to application/json for POST and PUT requests.
3. Use the request/response bodies as shown above.

---

## Test Suite Documentation
- **Location:** `tests/test_users.py`
- **Framework:** pytest + FastAPI TestClient
- **Coverage:**
  - Create user (valid and duplicate)
  - List users
  - Get user by ID (valid and not found)
  - Update user (valid and not found)
  - Delete user (valid and not found)
- **Edge Cases:**
  - Duplicate username/email
  - Access/update/delete non-existent user
  - Partial updates
  - Validation errors (invalid email, missing fields, etc.)

### Example Test (Create Duplicate User)
```python
def test_create_duplicate_user():
    client.post("/users/", json=user_payload(username="dupuser", email="dup@example.com"))
    response = client.post("/users/", json=user_payload(username="dupuser", email="dup@example.com"))
    assert response.status_code == 400
    assert "already exists" in response.text
```

---

## Evaluation of Error Handling
- **Properly Handles:**
  - Unique constraint violations (username/email)
  - Not found for all relevant endpoints
  - Validation errors on input
  - Database commit/rollback logic
- **Returns Correct HTTP Status Codes** for all edge cases.
- **Logs** all CRUD operations and warnings for not found cases.

---

## How to Explore Further
- **Run locally** and visit `/docs` for live API exploration.
- **Check tests** in `tests/test_users.py` for examples of edge case handling.
- **Review logs** for operation tracking and error diagnostics.
