import pytest
from django.contrib.auth.models import User
from api.models import FoodCategory, FoodItem, Order, OrderItem

@pytest.mark.django_db
def test_order_item_creation():
    user = User.objects.create_user(username="itemuser", password="pass123")
    category = FoodCategory.objects.create(name="Fast Food")

    food = FoodItem.objects.create(
        name="Rice",
        category=category,
        calories=200,
        protein=4.5,
        carbs=45.0,
        fats=1.2,
        price=50,
        is_available=True
    )

    order = Order.objects.create(user=user)

    item = OrderItem.objects.create(
        order=order,
        food=food,
        quantity=2,
        price=200
    )

    assert item.price == 200