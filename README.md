# DietFood Backend API

A Django REST Framework backend for a food ordering system with authentication, OTP verification, meal planning, order management, and payment handling.

---

## 🚀 Features

- User registration with email OTP verification
- JWT-based authentication (login)
- Food category & food item management
- Meal plan creation and retrieval
- Order & order item handling
- Order payment and cancellation flow
- Swagger API documentation
- Pytest-based automated testing with high coverage

---

## 🧭 User Journey (End-to-End API Flow)

This section explains how a user interacts with the system from registration to order completion.

---

## 👤 1. User Registration

### Register User

**Endpoint**

```
POST http://127.0.0.1:8000/api/user/register/
```

**Request Fields**

- username
- email
- password
- confirm_password

**Internal Flow**

- User is created with `is_active = False`
- A 6-digit OTP is generated
- OTP is saved in `EmailOTP` model:
  - expires in 2 minutes
  - `is_used = False`
- OTP is sent to the user’s email

✅ User is registered but cannot log in yet

---

## 🔐 2. OTP Verification

### Verify OTP

**Endpoint**

```
POST http://127.0.0.1:8000/verify-otp/
```

**Request Fields**

- email
- otp

**Validation Rules**

- OTP must exist
- OTP must match the user
- OTP must not be expired
- OTP must not be already used

**Success Result**

- OTP marked as `is_used = True`
- User account activated (`is_active = True`)

✅ User account is now verified

---

## 🔑 3. Login & Authentication

### Login User

**Endpoint**

```
POST http://127.0.0.1:8000/login/
```

**Request Body**

```json
{
  "email": "user@example.com",
  "password": "strongpassword"
}
```

**Response**

```json
{
  "refresh": "xxxxx",
  "access": "xxxxx"
}
```

✅ User receives JWT tokens and can access protected APIs

---

## 🍽️ 4. Food Browsing

### View Food Categories

**Endpoint**

```
GET /api/food-categories/
```

**Access**

- Public
- Authenticated users

### View Food Items

**Endpoint**

```
GET /api/food-items/
```

**Admin Permissions**
Only admins can:

- Create food categories and items
- Update food categories and items
- Delete food categories and items

---

## 📅 5. Meal Plan

### Create Meal Plan

**Endpoint**

```
POST /api/mealplans/
```

**Request Body**

```json
{
  "title": "Weekly Diet Plan",
  "food_items": [1, 3, 5]
}
```

**Meal Plan Includes**

- Title
- Multiple food items
- Linked to authenticated user

### Retrieve Meal Plan

**Endpoint**

```
GET /api/mealplans/{id}/
```

✅ Users can organize meals for planning purposes

---

## 🛒 6. Order Creation

### Create Order

**Endpoint**

```
POST /api/orders/
```

**Order Properties**

- Linked to authenticated user
- Initial status: `pending`
- `total_price` calculated automatically

**Sample Response**

```json
{
  "id": 12,
  "status": "pending",
  "total_price": "850.00"
}
```

---

## 📦 7. Order Items

### Add Item to Order

**Endpoint**

```
POST /api/order-items/
```

**Request Body**

```json
{
  "order": 12,
  "food": 3,
  "quantity": 2
}
```

**Validation Rules**

- Quantity must be greater than 0
- Food item must be available
- Price calculated automatically (`food.price × quantity`)

---

## 💳 8. Payment

### Pay for Order

**Endpoint**

```
PATCH /api/orders/{id}/pay/
```

**Result**

```
pending → paid
```

**Rule**

- Only the order owner can pay

---

## ❌ 9. Order Cancellation

### Cancel Order

**Endpoint**

```
PATCH /api/orders/{id}/cancel/
```

**Rules**

- Only the order owner can cancel
- Paid orders cannot be canceled again

---

## 🧑‍💼 10. Admin Order Management

### Update Order Status (Admin Only)

**Endpoint**

```
PATCH /api/orders/{id}/status/
```

**Request Body**

```json
{
  "status": "paid"
}
```

**Allowed Status Values**

- paid
- canceled

---

## 🔒 11. Authorization & Security

- JWT-based authentication (SimpleJWT)
- Role-based access control:
  - Admin
  - Authenticated User
  - Public (read-only)
- Custom permission:
  - `IsAdminOrReadOnly`

---

## 🧪 12. Testing & Quality Assurance

**Frameworks**

- pytest
- pytest-django

**Covered Areas**

- Registration & OTP verification
- Login & authentication
- CRUD operations
- Permissions
- Order & payment flow

**Run Tests & Coverage**

```bash
pytest --cov=api --cov-report=term-missing
pytest --cov=api --cov-report=html
```

✅ Current coverage: ~92%

---

## 🛠 Tech Stack

- Python 3.13
- Django 6.0
- Django REST Framework
- SimpleJWT
- drf-spectacular (Swagger)
- Pytest + pytest-django

---

## 📚 API Documentation

Swagger UI:

```
http://127.0.0.1:8000/api/docs/
```

---

## ⚙️ Setup Instructions

```bash
git clone https://github.com/shohan1138/2nd-week-23-30-dec-2025-.git
cd backend
python -m venv env
env\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

---

## 📌 Project Status

- ✅ Week-1: Authentication & OTP
- ✅ Week-2: Core APIs & Testing
- 🚀 Deployment: Pending
