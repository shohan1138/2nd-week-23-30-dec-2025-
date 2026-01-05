# DietFood Backend API

A Django REST Framework backend for a food ordering system with
authentication, OTP verification, order management, and payment status handling.

---

## 🚀 Features

- User registration with email OTP verification
- JWT authentication (login)
- Food category & food item management
- Meal plan APIs
- Order & order item handling
- Order payment and cancellation flow
- Swagger API documentation
- Pytest-based test coverage

---

## 🧭 User Journey (End-to-End API Flow)

This section describes how a user interacts with the system from registration to order completion.

---

### 👤 1. User Registration Journey

**Step 1: User Registers**

User submits:

- `username`
- `email`
- `password`
- `confirm_password`

**API Endpoint**
POST /api/register/

markdown
Copy code

**Internal Process**

- User is created with `is_active = False`
- A 6-digit OTP is generated
- OTP is saved in `EmailOTP` model:
  - expiry time: 2 minutes
  - `is_used = False`
- OTP is sent to user email

✅ User is registered but cannot log in yet

---

### 🔐 2. OTP Verification Journey

**Step 2: User Verifies OTP**

User submits:

- `email`
- `otp`

**API Endpoint**
POST /api/verify-otp/

markdown
Copy code

**Validation Rules**

- OTP must exist
- OTP must match the user
- OTP must not be expired
- OTP must not be already used

**Success Outcome**

- OTP marked as `is_used = True`
- User account activated (`is_active = True`)

✅ User account is now verified

---

🔑 3. Login & Authentication Journey
▶ Step 3: User Logs In

Endpoint

POST /api/login/

Request Body

{
"email": "user@example.com",
"password": "strongpassword"
}

Success Response

{
"refresh": "xxxxx",
"access": "xxxxx"
}

Result

✅ User receives JWT tokens

✅ Can access protected APIs

🍽️ 4. Food Browsing Journey
▶ Step 4: View Food Categories

Endpoint

GET /api/food-categories/

Access Level

🌐 Anonymous users

🔐 Authenticated users

▶ Step 5: View Food Items

Endpoint

GET /api/food-items/

Admin Capabilities
Only admin users can:

➕ Create food categories & items

✏️ Update food categories & items

❌ Delete food categories & items

📅 5. Meal Plan Journey
▶ Step 6: Create Meal Plan

Endpoint

POST /api/mealplans/

Request Body

{
"title": "Weekly Diet Plan",
"food_items": [1, 3, 5]
}

Meal Plan Contains

Title

Multiple food items

Associated authenticated user

▶ Step 7: Retrieve Meal Plan

Endpoint

GET /api/mealplans/{id}/

Result

✅ Users can organize meals for planning purposes

🛒 6. Order Creation Journey
▶ Step 8: Create Order

Endpoint

POST /api/orders/

Order Properties

Linked to authenticated user

Initial status: pending

total_price calculated automatically

Sample Response

{
"id": 12,
"status": "pending",
"total_price": "850.00"
}

📦 7. Order Item Journey
▶ Step 9: Add Items to Order

Endpoint

POST /api/order-items/

Request Body

{
"order": 12,
"food": 3,
"quantity": 2
}

Validation Rules

Quantity > 0

Food item must be available

Price auto-calculated
(food.price × quantity)

💳 8. Payment Journey
▶ Step 10: Pay for Order

Endpoint

PATCH /api/orders/{id}/pay/

Outcome

pending → paid

Rule

Only the order owner can pay

❌ 9. Order Cancellation Journey
▶ Step 11: Cancel Order

Endpoint

PATCH /api/orders/{id}/cancel/

Rules

Only order owner can cancel

Paid orders ❌ cannot be canceled again

🧑‍💼 10. Admin Order Management
▶ Step 12: Update Order Status (Admin Only)

Endpoint

PATCH /api/orders/{id}/status/

Request Body

{
"status": "paid"
}

Admin Can Set

paid

canceled

🔒 11. Authorization & Security

Authentication

JWT-based authentication (SimpleJWT)

Role-Based Access

👑 Admin

👤 Authenticated User

🌐 Public (read-only)

Custom Permission

IsAdminOrReadOnly

🧪 12. Testing & Quality Assurance

Frameworks

pytest

pytest-django

Covered Areas

Registration & OTP verification

Login & authentication

CRUD operations

Permissions

Order & payment flow

Test Coverage

pytest --cov=api --cov-report=term-missing
pytest --cov=api --cov-report=html

Current Coverage
✅ ~92%

🛠 Tech Stack

Python 3.13

Django 6.0

Django REST Framework

SimpleJWT

drf-spectacular (Swagger)

Pytest + pytest-django

📚 API Documentation

Swagger UI

http://127.0.0.1:8000/api/docs/

⚙️ Setup Instructions
git clone https://github.com/shohan1138/2nd-week-23-30-dec-2025-.git
cd backend
python -m venv env
env\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

📌 Project Status

✅ Week-1: Authentication & OTP

✅ Week-2: Core APIs & Testing

🚀 Deployment: Pending
