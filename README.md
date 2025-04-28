
# Game of Thrones Character API

This project is a RESTful API built with FastAPI and SQLite. It manages Game of Thrones characters and supports full CRUD operations, JWT Authentication, filtering, sorting, and pagination.

## Features

- Fetch all characters (with pagination, filtering, sorting)
- Fetch a character by ID
- Create new characters (protected with JWT)
- Update existing characters (protected with JWT)
- Delete characters (protected with JWT)
- Authentication via JSON Web Tokens (JWT)
- SQLite database integration
- Clean error handling

## Technologies

- Python 3.11
- FastAPI
- SQLite
- SQLAlchemy
- Python-JOSE (for JWT)
- Uvicorn

## Setup

1. Clone the repository:

```bash
git clone <repository_url>
cd got-characters-api
```

2. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
Install dependencies:
```
3. Install dependencies:

```bash
pip install -r requirements.txt
Start the application:
```
4. Start the application:


```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```
The API will be available at: http://localhost:8000
FastAPI's Swagger UI is available at: http://localhost:8000/docs


## Predefined Users

Username | Password | Role
--- | --- | ---
admin | adminpass | admin
user | userpass | user


## Authentication
1. Make a POST request to /login with the following body (Content-Type: x-www-form-urlencoded):

```bash
username=admin&password=adminpass
```

You will receive a JSON response:

```json
{
  "access_token": "<JWT_TOKEN>",
  "token_type": "bearer"
}
```

Use this token in the Authorization header for protected routes:

```bash
Authorization: Bearer <JWT_TOKEN>
```

## API Endpoints

Method | Endpoint | Protected? | Description
---|---|---|---
POST | /login | ❌ | Get JWT Token
GET | /characters | ❌ | Get all characters with optional pagination, filtering, sorting
GET | /characters/{id} | ❌ | Get character by ID
POST | /characters | ✅ | Create a new character
PATCH | /characters/{id} | ✅ | Update character fields
DELETE | /characters/{id} | ✅ | Delete a character

## Example Protected Request
```bash
curl -X POST "http://localhost:8000/characters" \
-H "Authorization: Bearer <your_token>" \
-H "Content-Type: application/json" \
-d '{
    "name": "Arya Stark",
    "house": "Stark",
    "animal": "Direwolf",
    "symbol": "Wolf",
    "nickname": "No One",
    "role": "Assassin",
    "age": 18,
    "death": null,
    "strength": "Stealth"
}'
```





