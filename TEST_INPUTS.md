

# **Sample Test Inputs for Ecommerce REST API**

### **1️⃣ User Endpoints**

#### **a) Create User**

**Endpoint:** `POST /users/register`
**Purpose:** Create a new user

**Sample Input:**

```json
{
  "email": "john@example.com",
  "password": "Password123!"
}
```

**Expectations:**

* Returns 201 Created
* Response includes `id` and `email` (UserOut schema)
* Password is hashed (not returned)

---

#### **b) Login User**

**Endpoint:** `POST /users/login`
**Purpose:** Authenticate user

**Sample Input:**

```json
{
  "email": "john@example.com",
  "password": "Password123!"
}
```

**Expectations:**

* Returns JWT token (`access_token`) and type `"bearer"`
* Can be used in `Authorization: Bearer <token>` header for all protected endpoints

---

#### **c) Get Current User (Me)**

**Endpoint:** `GET /users/me`
**Headers:** `Authorization: Bearer <access_token>`
**Purpose:** Get current logged-in user

**Expectations:**

* Returns UserOut (`id` and `email`)
* Should match the logged-in user

---

### **2️⃣ Product Endpoints**

#### **a) Create Product**

**Endpoint:** `POST /products/`
**Headers:** `Authorization: Bearer <admin_token>` (if admin protected)

**Sample Input:**

```json
{
  "name": "Laptop",
  "description": "Gaming laptop",
  "price": 1200.50,
  "stock": 5
}
```

**Expectations:**

* Returns ProductOut including `id`, `name`, `price`, `stock`, `description`

---

#### **b) Get All Products**

**Endpoint:** `GET /products/`

**Expectations:**

* Returns list of ProductOut
* Each product has `id`, `name`, `price`, `stock`, `description`

---

#### **c) Get Single Product**

**Endpoint:** `GET /products/{product_id}`

**Sample:** `GET /products/1`

**Expectations:**

* Returns ProductOut of requested product
* 404 if product not found

---

#### **d) Update Product**

**Endpoint:** `PUT /products/{product_id}`

**Sample Input:**

```json
{
  "name": "Laptop Pro",
  "description": "Updated gaming laptop",
  "price": 1300.00,
  "stock": 3
}
```

**Expectations:**

* Returns updated ProductOut
* Fields reflect the update

---

#### **e) Delete Product**

**Endpoint:** `DELETE /products/{product_id}`

**Expectations:**

* Returns `{"message": "Product deleted"}`
* Product removed from GET list

---

### **3️⃣ Cart Endpoints**

#### **a) Add to Cart**

**Endpoint:** `POST /cart/`
**Headers:** `Authorization: Bearer <token>`

**Sample Input:**

```json
{
  "product_id": 1,
  "quantity": 2
}
```

**Expectations:**

* Adds product to user’s cart
* Returns `{"message": "Added to cart"}`

---

#### **b) View Cart**

**Endpoint:** `GET /cart/`
**Headers:** `Authorization: Bearer <token>`

**Expectations:**

* Returns list of CartItemOut
* Each item includes `product` nested object

---

#### **c) Checkout Cart**

**Endpoint:** `POST /cart/checkout`
**Headers:** `Authorization: Bearer <token>`

**Expectations:**

* Returns OrderOut with:

  * `id`
  * `user_id`
  * `total_amount`
  * `items`: List of OrderItemOut including `product` details

**Sample Response (Partial)**

```json
{
  "id": 1,
  "user_id": 1,
  "total_amount": 2401.0,
  "items": [
    {
      "id": 1,
      "order_id": 1,
      "product_id": 1,
      "quantity": 2,
      "price": 1200.50,
      "product": {
        "id": 1,
        "name": "Laptop",
        "description": "Gaming laptop",
        "price": 1200.50,
        "stock": 3
      }
    }
  ]
}
```

---

### **4️⃣ Orders Endpoints**

#### **a) Get User Orders**

**Endpoint:** `GET /users/orders`
**Headers:** `Authorization: Bearer <token>`

**Expectations:**

* Returns list of OrderOut
* Each order contains items and nested product info

---

### **5️⃣ Notes for Manual Testing via Swagger / Postman**

1. Always include **Authorization: Bearer <token>** after login.
2. Test **invalid inputs**: negative quantities, missing fields, invalid emails, duplicate products.
3. Test **edge cases**: empty cart checkout, out-of-stock products, deleting a product in cart.
4. Check **response structure** matches schemas: `UserOut`, `ProductOut`, `CartItemOut`, `OrderOut`.

---


