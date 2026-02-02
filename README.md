# Ecommerce REST API – Test Engineer Guide

This document is written for **Manual Test Engineers** and **Automation Test Engineers**.
It explains how to start the server, what APIs are available, and what to test with clear expectations.

---

## 1. Starting the Server (Docker – Recommended)

### Prerequisites

* macOS
* Docker Desktop installed and running

### Directory Preparation (One-Time)

The database is persisted on the host machine.

```bash
mkdir -p /Users/smruti/Dev/2mpattanaik/ecommerce_rest_api/docker_data
```

### Build and Start the Server

From the project root directory:

```bash
docker-compose up --build
```

### Expected Result

* Server starts on **port 9000**
* SQLite database file is created at:

  ```
  /Users/smruti/Dev/2mpattanaik/ecommerce_rest_api/docker_data/shop.db
  ```
* Swagger UI is available at:

  ```
  http://localhost:9000/docs
  ```

> ⚠️ Data persists across container restarts. Do NOT delete the DB file unless intentionally resetting data.

---

## 2. Authentication Model (Important for Testing)

* The application uses **JWT Bearer Token authentication**
* All business APIs require login
* Token must be sent in header:

```
Authorization: Bearer <access_token>
```

Swagger UI supports this via the **Authorize 🔒** button.

---

## 3. Available APIs

### Authentication APIs

| Method | Endpoint     | Description                    |
| ------ | ------------ | ------------------------------ |
| POST   | /users/      | Create a new user (Public)     |
| POST   | /auth/login  | Login and get JWT token        |
| POST   | /auth/logout | Logout (client discards token) |
| GET    | /users/me    | Get current logged-in user     |

---

### Product APIs (Protected)

| Method | Endpoint       | Description       |
| ------ | -------------- | ----------------- |
| POST   | /products/     | Create a product  |
| GET    | /products/     | List all products |
| PUT    | /products/{id} | Update product    |
| DELETE | /products/{id} | Delete product    |

---

### Cart APIs (Protected)

| Method | Endpoint       | Description             |
| ------ | -------------- | ----------------------- |
| POST   | /cart/         | Add item to cart        |
| GET    | /cart/         | View cart items         |
| POST   | /cart/checkout | Checkout and clear cart |

---

## 4. Suggested Test Flow (Manual & Automation)

### Step 1: User Creation

* Call **POST /users/**
* Expectation:

  * HTTP 200
  * User created successfully

---

### Step 2: Login

* Call **POST /auth/login**
* Provide valid credentials
* Expectation:

  * HTTP 200
  * `access_token` returned

---

### Step 3: Authorization

* Click **Authorize** in Swagger
* Paste token as:

  ```
  Bearer <token>
  ```
* Expectation:

  * Authorized APIs accessible

---

### Step 4: Product Management

* Create a product
* List products
* Update product
* Delete product

**Expectations:**

* CRUD operations succeed with valid token
* Unauthorized requests return **401**

---

### Step 5: Cart Operations

* Add product to cart
* View cart
* Checkout

**Expectations:**

* Cart is user-specific
* Checkout clears cart
* Cart remains empty after checkout

---

## 5. Negative / Security Test Scenarios

Manual & Automation engineers should verify:

* ❌ Access protected APIs **without token** → 401
* ❌ Use expired or invalid token → 401
* ❌ Access cart data across users → Not allowed
* ❌ Delete product without login → 401

---

## 6. Persistence Expectations

* Stop Docker container
* Restart container

**Expected:**

* Users remain
* Products remain
* Cart persists unless checkout was completed

---

## 7. Automation Testing Notes

* Token can be extracted from `/auth/login`
* Token must be injected in request headers
* Database state persists → tests should be idempotent
* Cleanup should be done via APIs, not DB deletion

---

## 8. Common Troubleshooting

| Issue              | Resolution                       |
| ------------------ | -------------------------------- |
| Port not reachable | Ensure Docker is running         |
| 401 Unauthorized   | Check Bearer token               |
| DB not updating    | Verify docker_data volume exists |

---

## 9. Swagger Reference

Swagger UI:

```
http://localhost:9000/docs
```

OpenAPI Spec:

```
http://localhost:9000/openapi.json
```

---

## Summary

* Docker is the preferred way to run the application
* Authentication is mandatory for all business APIs
* Data is persistent across restarts
* API behavior is predictable and automation-friendly


