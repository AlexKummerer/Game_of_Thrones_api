# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

Start the development server:
```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at http://localhost:8000 with interactive docs at http://localhost:8000/docs

## Architecture Overview

This is a FastAPI-based Game of Thrones character management API with SQLite database integration and JWT authentication.

### Core Structure
- **app.py**: Main FastAPI application with all route handlers and exception handling
- **db/database.py**: SQLAlchemy database configuration and initialization
- **models/**: Contains both plain Python character class and SQLAlchemy ORM model
  - `character.py`: Plain Python class for character representation
  - `character_db.py`: SQLAlchemy ORM model for database operations
- **services/**: Business logic layer
  - `character_service.py`: Core CRUD operations with filtering, sorting, and pagination
  - `admin_service.py`: Admin-specific operations like JSON data loading
  - `data_loader.py`: Utility for loading character data from JSON files
- **auth/**: Authentication system
  - `jwt_handler.py`: JWT token creation and validation
  - `dependencies.py`: Authentication dependencies for route protection
  - `users.py`: Predefined user accounts
- **controllers/**: Additional controller logic
- **data/**: Contains `characters.json` with initial character data

### Authentication
Uses JWT tokens with predefined users:
- admin/adminpass (admin role)
- user/userpass (user role)

All character modification endpoints (POST, PATCH, DELETE) require authentication. Admin-only endpoints require admin role.

### Database
SQLite database (`characters.db`) with SQLAlchemy ORM. Database is initialized on application startup via `init_db()` in app.py.

### Key Features
- Full CRUD operations for characters
- Filtering by name, house, role, age (with comparison operators)
- Sorting (ascending/descending) by any character field
- Pagination with limit/skip
- Duplicate name prevention on character creation
- Admin-only JSON bulk loading functionality