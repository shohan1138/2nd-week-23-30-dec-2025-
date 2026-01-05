import pytest
from api.serializers import OrderItemSerializer
from api.models import FoodCategory, FoodItem

@pytest.mark.django_db
def test_orderitem_serializer_invalid_quantity():
    category = FoodCategory.objects.create(name="Cat")
    food = FoodItem.objects.create(
        category=category,
        name="Rice",
        calories=200,
        protein=5,
        carbs=40,
        fats=2,
        price=50
    )

    serializer = OrderItemSerializer(data={
        "food": food.id,
        "quantity": 0
    })

    assert not serializer.is_valid()

@pytest.mark.django_db
def test_orderitem_serializer_unavailable_food():
    category = FoodCategory.objects.create(name="Cat")
    food = FoodItem.objects.create(
        category=category,
        name="Fish",
        calories=250,
        protein=30,
        carbs=0,
        fats=5,
        price=200,
        is_available=False
    )

    serializer = OrderItemSerializer(data={
        "food": food.id,
        "quantity": 1
    })

    assert not serializer.is_valid()