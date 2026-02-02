Perfect! Let’s create a **comprehensive sample test input table** for **all APIs** in your FastAPI e-commerce app. This can be used by **manual testers via Swagger/Postman** or **automation engineers via Playwright**. I’ll include **method, endpoint, headers, body, and expected response details**.

---

# **Sample Test Inputs for E-Commerce REST API**

---

## **1️⃣ User APIs**

| Action           | Method | Endpoint          | Headers                         | Body (JSON)                                                 | Expected Result / Notes                                              |
| ---------------- | ------ | ----------------- | ------------------------------- | ----------------------------------------------------------- | -------------------------------------------------------------------- |
| Register User    | POST   | `/users/register` | None                            | `{ "email": "alice@example.com", "password": "Alice123!" }` | Returns `UserOut` with `id` and `email`. 400 if email already exists |
| Login User       | POST   | `/users/login`    | None                            | `{ "email": "alice@example.com", "password": "Alice123!" }` | Returns `TokenOut` with `access_token` and `token_type: "bearer"`    |
| Get Current User | GET    | `/users/me`       | `Authorization: Bearer <token>` | None                                                        | Returns `UserOut` for logged-in user. 401 if token missing/invalid   |
| Get User Orders  | GET    | `/users/orders`   | `Authorization: Bearer <token>` | None                                                        | Returns list of `OrderOut`. Empty list if no orders                  |

---

## **2️⃣ Product APIs**

| Action            | Method | Endpoint         | Headers                         | Body (JSON)                                                                             | Expected Result / Notes                       |
| ----------------- | ------ | ---------------- | ------------------------------- | --------------------------------------------------------------------------------------- | --------------------------------------------- |
| Create Product    | POST   | `/products/`     | `Authorization: Bearer <token>` | `{ "name": "Laptop", "description": "Intel i7, 16GB RAM", "price": 1500, "stock": 10 }` | Returns `ProductOut` with product details     |
| List Products     | GET    | `/products/`     | `Authorization: Bearer <token>` | None                                                                                    | Returns list of all products (`ProductOut`)   |
| Get Product by ID | GET    | `/products/{id}` | `Authorization: Bearer <token>` | None                                                                                    | Returns single `ProductOut`. 404 if not found |
| Update Product    | PUT    | `/products/{id}` | `Authorization: Bearer <token>` | `{ "name": "Laptop Pro", "price": 1600, "stock": 8 }`                                   | Updates and returns updated `ProductOut`      |
| Delete Product    | DELETE | `/products/{id}` | `Authorization: Bearer <token>` | None                                                                                    | 200 OK if deleted, 404 if not found           |

---

## **3️⃣ Cart APIs**

| Action           | Method | Endpoint         | Headers                         | Body (JSON)                          | Expected Result / Notes                                                             |
| ---------------- | ------ | ---------------- | ------------------------------- | ------------------------------------ | ----------------------------------------------------------------------------------- |
| Add Item to Cart | POST   | `/cart/`         | `Authorization: Bearer <token>` | `{ "product_id": 1, "quantity": 2 }` | Returns `CartItemOut` with product_id, quantity, price, total_price                 |
| View Cart        | GET    | `/cart/`         | `Authorization: Bearer <token>` | None                                 | Returns list of all cart items (`CartItemOut`)                                      |
| Checkout Cart    | POST   | `/cart/checkout` | `Authorization: Bearer <token>` | None                                 | Creates `Order` and `OrderItem`, clears cart. Returns `OrderOut`. 400 if cart empty |

---

## **4️⃣ Notes for Manual Testing (Swagger/Postman)**

1. Always **register a user first** → then login to get token.
2. Use **Bearer token** in Authorization header for all protected endpoints.

   * Example: `Authorization: Bearer eyJhbGciOiJI...`
3. **Product stock** should decrement correctly when adding/checkout (if implemented).
4. **Cart should be empty** after checkout.
5. `/users/orders` should reflect newly created orders with correct items and prices.

---

## **5️⃣ Notes for Automation Testing (Playwright / Scripts)**

1. **Set base URL:** `http://localhost:9000`

2. **Steps for a full e2e test:**

   * Register a user
   * Login and save token
   * Create 1–2 products
   * Add products to cart
   * View cart and assert totals
   * Checkout
   * Verify order appears in `/users/orders`
   * Verify cart is empty after checkout

3. **Assertions to consider:**

   * Status codes (`200/201/400/401`)
   * JSON schema matches `UserOut`, `ProductOut`, `CartItemOut`, `OrderOut`
   * Cart totals = sum of `price_per_unit * quantity`
   * Token-protected endpoints fail if **Authorization header missing or invalid**

---


