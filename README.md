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

## 🧪 Running Tests & Coverage

```bash
pytest --cov=api --cov-report=term-missing
Current coverage: ~90%

⚙️ Setup Instructions
bash
Copy code
git clone <repo-url>
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
```
