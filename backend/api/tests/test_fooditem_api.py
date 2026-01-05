import pytest
from django.urls import reverse
from api.models import FoodCategory, FoodItem
from rest_framework.test import APIClient
from django.contrib.auth.models import User

client = APIClient()

@pytest.mark.django_db
def test_list_food_items():
    cat = FoodCategory.objects.create(name="Lunch")
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

@pytest.mark.django_db
def test_create_fooditem_invalid_data():
    cat = FoodCategory.objects.create(name="lunch")
    user = User.objects.create_user(username="admin", password="pass")
    client=APIClient()
    client.force_authenticate(user=user)
    url = reverse("fooditem-list")
    data = {
        "name": "Chicken",
        "category": cat.id,
        "calories": 250,
        "protein": 27.0,
        "carbs": 0.0,
        "fats": 15.0,
        
        "is_available": True
    }
    response = client.post(url, data, format='json')
    assert response.status_code == 403
    assert "detail" in response.data


@pytest.mark.django_db
def test_fooditem_negative_price():
    client = APIClient()
    user = User.objects.create_user(username="admin", password="pass")
    client.force_authenticate(user=user)

    response = client.post(
        reverse("fooditem-list"),
        {
            "name": "Burger",
            "price": -10,
            "calories": 300,
            "protein": 12,
            "carbs": 30,
            "fats": 15
        },
        format="json"
    )

    assert response.status_code == 403