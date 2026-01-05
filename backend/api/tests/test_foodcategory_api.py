from urllib import response
import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from api.models import FoodCategory

client = APIClient()

@pytest.mark.django_db
def test_list_food_categories():
    FoodCategory.objects.create(name="Breakfast")
    FoodCategory.objects.create(name="Lunch")

    response = client.get(reverse("foodcategory-list"))

    assert response.status_code == 200
    assert response.data["count"] == 2
    assert len(response.data["results"]) == 2

@pytest.mark.django_db
def test_foodcategory_list_empty():
    client = APIClient()
    url = reverse("foodcategory-list")

    response = client.get(url)

    assert response.status_code == 200
    assert response.data["count"] == 0
    assert response.data["results"] == []