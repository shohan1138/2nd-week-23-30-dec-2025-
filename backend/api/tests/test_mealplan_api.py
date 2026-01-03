import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from api.models import MealPlan

client = APIClient()

@pytest.mark.django_db
def test_mealplan_retrieve():
    user = User.objects.create_user(
        username="mealuser",
        password="pass123"
    )

    plan = MealPlan.objects.create(
        user=user,
        title="Weekly Plan"
    )

    response = client.get(
        reverse("mealplan-detail", args=[plan.id])
    )

    assert response.status_code == 200
    assert response.data["title"] == "Weekly Plan"

@pytest.fixture
def user():
    return User.objects.create_user(
        username="mealuser",
        password="pass123"
    )
@pytest.mark.django_db
def test_mealplan_retrieve(user):
    plan = MealPlan.objects.create(
        user=user,
        title="Weekly Plan"
    )