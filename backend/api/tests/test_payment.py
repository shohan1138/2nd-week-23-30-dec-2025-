import pytest
from django.contrib.auth.models import User
from api.models import Order

@pytest.mark.django_db
def test_order_payment():
    # Create a test user
    user = User.objects.create_user(username='testuser', password='testpass')

    # Create a test order
    order = Order.objects.create(user=user, total_price=100.00, status='pending')

    # Simulate payment process
    order.status = 'paid'
    order.save()

    # Fetch the updated order from the database
    updated_order = Order.objects.get(id=order.id)

    # Assert that the order status is updated to 'paid'
    assert updated_order.status == 'paid'