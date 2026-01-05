import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from api.models import MealPlan
from django.contrib.auth.models import User
client = APIClient()

@pytest.mark.django_db
def test_mealplan_retrieve():
    user = User.objects.create_user(username="u", password="pass")

    plan = MealPlan.objects.create(
        user=user,
        title="Weekly Plan"
    )

    response = client.get(reverse("mealplan-detail", args=[plan.id]))

    assert response.status_code == 200
    assert response.data["title"] == "Weekly Plan"

@pytest.mark.django_db
def test_order_list_unauthorized():
    client = APIClient()
    url = reverse("order-list")
    response = client.get(url)
    assert response.status_code in [401, 403]