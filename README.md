# FastAPI Product Management API

A RESTful API built using **FastAPI** for managing products and users with JWT authentication.

## Features

- User authentication with JWT
- CRUD operations for products and users
- Secure password hashing with bcrypt

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo-url.git
   cd your-repo-directory
   ```

2. Set up a virtual environment and install dependencies:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # For Linux/MacOS
   venv\Scripts\activate     # For Windows
   pip install -r requirements.txt
   ```

3. Configure your `.env` file for sensitive information (e.g., `DATABASE_URL`, `SECRET_KEY`).

## API Endpoints

### Authentication

- **POST /login**: Login to get a JWT token.
  - Request: `{ "username": "user@example.com", "password": "your_password" }`
  - Response: `{ "access_token": "your_jwt_token", "token_type": "bearer" }`

### User Management

- **POST /user**: Create a new user.
- **GET /user/{id}**: Get user by ID.
- **PUT /user/{id}**: Update user by ID.
- **DELETE /user/{id}**: Delete user by ID.

### Product Management

- **GET /products**: Get all products.
- **POST /products**: Create a new product.
- **GET /products/{id}**: Get product by ID.
- **PUT /products/{id}**: Update product by ID.
- **DELETE /products/{id}**: Delete product by ID.

## Running the Server

To run the FastAPI development server:

```bash
uvicorn main:app --reload
```

Access the API at `http://localhost:8000`.
