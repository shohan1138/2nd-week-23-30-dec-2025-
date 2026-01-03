import pytest
from django.urls import reverse
from api.models import FoodCategory, FoodItem
from rest_framework.test import APIClient

client = APIClient()

@pytest.mark.django_db
def test_list_food_items():
    cat = FoodCategory.objects.create(name="Dinner")
    FoodItem.objects.create(        
        name="Rice",
        category=cat,
        calories=200,
        protein=4.5,
        carbs=45.0,
        fats=1.2,
        price=50,
        is_available=True
    )

    response = client.get(reverse("fooditem-list"))
    assert response.status_code == 200
    assert response.data["results"][0]["name"] == "Rice"