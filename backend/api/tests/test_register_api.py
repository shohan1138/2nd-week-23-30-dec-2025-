import pytest
from django.urls import reverse
from rest_framework.test import APIClient

client = APIClient()

@pytest.mark.django_db
def test_register_success():
    payload = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "strongpassword123",
        "confirm_password": "strongpassword123"
    }
    response = client.post(reverse("register"), payload, format='json')

    assert response.status_code == 201  
    assert response.data["email"] == "test@example.com"

@pytest.mark.django_db
def test_register_email_duplicate():
    payload = {
        "username": "testuser1",
        "email": "duplicate@example.com",
        "password": "strongpassword123",
        "confirm_password": "strongpassword123"
    }
    client.post(reverse("register"), payload, format='json')
    response = client.post(reverse("register"), payload, format='json')
    assert response.status_code == 400
    assert "email" in response.data
@pytest.mark.django_db
def test_register_password_mismatch():
    payload = {
        "username": "testuser2",
        "email": "test2@example.com",
        "password": "strongpassword123",
        "confirm_password": "wrongpassword"
    }
    response = client.post(reverse("register"), payload, format='json')

    assert response.status_code == 400
    assert "non_field_errors" in response.data