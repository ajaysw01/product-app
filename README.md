# Product Management API

## Overview
This API provides endpoints for managing products and users in an application. It includes features such as user authentication, CRUD operations for users and products, and export functionality for product data.

---

## Authentication
All protected routes require a valid JWT token for access. Tokens are generated upon successful login.

---

## Endpoints

### **1. Create User**
**Request:**
```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/users/' \
  -H 'Content-Type: application/json' \
  -d '{
    "name": "John Doe",
    "email": "john.doe@example.com",
    "password": "securepassword"
  }'
```

**Response:**
```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john.doe@example.com"
}
```

---

### **2. User Login**
**Request:**
```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/login' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'username=john.doe@example.com&password=securepassword'
```

**Response:**
```json
{
  "access_token": "your-jwt-token",
  "token_type": "bearer"
}
```

---

### **3. Create Product**
**Request:**
```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/products/' \
  -H 'Authorization: Bearer your-jwt-token' \
  -H 'Content-Type: application/json' \
  -d '{
    "name": "Product A",
    "description": "This is Product A",
    "price": 99.99
  }'
```

**Response:**
```json
{
  "id": 1,
  "name": "Product A",
  "description": "This is Product A",
  "price": 99.99,
  "user_id": 1
}
```

---

### **4. Delete Product**
**Request:**
```bash
curl -X 'DELETE' \
  'http://127.0.0.1:8000/products/1' \
  -H 'Authorization: Bearer your-jwt-token'
```

**Response:**
```json
{
  "message": "Product deleted successfully"
}
```

---

### **5. Export Products to CSV or JSON**

#### **Export Products to CSV**
**Request:**
```bash
curl -X 'GET' \
  'http://127.0.0.1:8000/products/export?file_format=csv' \
  -H 'Authorization: Bearer your-jwt-token'
```

**Response:**
```json
{
  "message": "Products exported successfully",
  "file_path": "exports/products_<timestamp>.csv"
}
```

---

#### **Export Products to JSON**
**Request:**
```bash
curl -X 'GET' \
  'http://127.0.0.1:8000/products/export?file_format=json' \
  -H 'Authorization: Bearer your-jwt-token'
```

**Response:**
```json
{
  "message": "Products exported successfully",
  "file_path": "exports/products_<timestamp>.json"
}
```

---

## Validations
1. **User Creation**
   - Email must be unique.
   - Password is hashed before storage.

2. **Login**
   - Valid email and password are required.

3. **Product Creation**
   - Product name, description, and price are mandatory.
   - Products are linked to the currently logged-in user.

4. **Delete Product**
   - Only the owner of the product can delete it.

5. **Export Products**
   - Requires a valid JWT token.
   - Supports `csv` and `json` formats.

---

## Folder for Exported Files
All exported files are stored in the `exports` folder within the project directory.


