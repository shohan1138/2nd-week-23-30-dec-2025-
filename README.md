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

### 🔑 3. Login & Authentication Journey

**Step 3: User Logs In**

User submits:

- `email`
- `password`

**API Endpoint**
POST /api/login/

pgsql
Copy code

**Checks Performed**

- Email exists
- Password is correct
- Account is OTP verified

**Success Response**

````json
{
  "refresh": "xxxxx",
  "access": "xxxxx"
}
✅ User receives JWT tokens and can access protected APIs

🍽️ 4. Food Browsing Journey
Step 4: View Food Categories

bash
Copy code
GET /api/food-categories/
Accessible by:

Anonymous users

Authenticated users

Step 5: View Food Items

bash
Copy code
GET /api/food-items/
Admin Capabilities
Only admin users can:

Create

Update

Delete food categories and food items

📅 5. Meal Plan Journey
Step 6: Create Meal Plan

bash
Copy code
POST /api/mealplans/
Meal Plan contains:

Title

Multiple food items

Associated user

Step 7: Retrieve Meal Plan

bash
Copy code
GET /api/mealplans/{id}/
✅ Users can organize meals for planning purposes

🛒 6. Order Creation Journey
Step 8: Create Order

bash
Copy code
POST /api/orders/
Order properties:

Linked to authenticated user

Initial status: pending

total_price calculated automatically

📦 7. Order Item Journey
Step 9: Add Items to Order

bash
Copy code
POST /api/order-items/
Validation Rules

Quantity must be greater than 0

Food item must be available

Price calculated automatically (food.price × quantity)

💳 8. Payment Journey
Step 10: Pay for Order

bash
Copy code
PATCH /api/orders/{id}/pay/
Outcome

nginx
Copy code
pending → paid
❌ 9. Order Cancellation Journey
Step 11: Cancel Order

bash
Copy code
PATCH /api/orders/{id}/cancel/
Rules:

Only the order owner can cancel

Paid orders cannot be canceled again

🧑‍💼 10. Admin Order Management
Step 12: Update Order Status (Admin)

bash
Copy code
PATCH /api/orders/{id}/status/
Admin can set:

paid

canceled

🔒 11. Authorization & Security
JWT-based authentication

Role-based access control:

Admin

Authenticated user

Public (read-only)

Custom permission:

IsAdminOrReadOnly

🧪 12. Testing & Quality Assurance
Testing framework: pytest, pytest-django

Covered areas:

Registration & OTP verification

Login & authentication

CRUD operations

Permissions

Order & payment flow

Current test coverage: ~92%

```bash
pytest --cov=api --cov-report=term-missing
pytest --cov=api --cov-report=html

## 🛠 Tech Stack

- Python 3.13
- Django 6.0
- Django REST Framework
- SimpleJWT
- drf-spectacular (Swagger)
- Pytest + pytest-django

---

## 📚 API Documentation

Swagger UI available at:

http://127.0.0.1:8000/api/docs/

yaml
Copy code

---


⚙️ Setup Instructions
bash
Copy code
git clone <https://github.com/shohan1138/2nd-week-23-30-dec-2025-.git>
cd backend
python -m venv env
env\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

📌 Project Status
Week-1: Authentication & OTP ✅

Week-2: Core APIs & testing ✅

Deployment: Pending
````
