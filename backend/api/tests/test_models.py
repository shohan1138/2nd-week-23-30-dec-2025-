import pytest
from django.contrib.auth.models import User
from api.models import (
    FoodCategory, FoodItem, MealPlan, Order, OrderItem
)

@pytest.mark.django_db
def test_model_str_methods():
    user = User.objects.create_user(username="u", password="123")

    category = FoodCategory.objects.create(name="Fast Food")
    food = FoodItem.objects.create(
        category=category,
        name="Burger",
        calories=300,
        protein=15,
        carbs=30,
        fats=10,
        price=150
    )
    meal = MealPlan.objects.create(user=user, title="My Plan")
    order = Order.objects.create(user=user)
    item = OrderItem.objects.create(order=order, food=food, quantity=2, price=300)

    assert str(category) == "Fast Food"
    assert str(food) == "Burger"
    assert str(meal) == "My Plan"
    assert "Order" in str(order)
    assert "Burger" in str(item)