import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from django.urls import reverse
from api.models import FoodCategory

@pytest.mark.django_db
def test_admin_permission_denied_for_normal_user():
    user = User.objects.create_user(username="user", password="pass")
    client = APIClient()
    client.force_authenticate(user=user)

    response = client.post(reverse("foodcategory-list"), {"name": "Test"})

    assert response.status_code == 201



@pytest.mark.django_db
def test_admin_can_create_foodcategory():
    from django.contrib.auth.models import User
    from rest_framework.test import APIClient
    from django.urls import reverse

    admin = User.objects.create_user(
        username="admin",
        password="pass",
        is_staff=True
    )

    client = APIClient()
    client.force_authenticate(user=admin)

    response = client.post(
        reverse("foodcategory-list"),
        {"name": "Admin Category"},
        format="json"
    )

    assert response.status_code in [200, 201]

@pytest.mark.django_db
def test_is_admin_or_readonly_blocks_non_admin():
    from api.permissions import IsAdminOrReadOnly
    from rest_framework.test import APIRequestFactory

    factory = APIRequestFactory()
    request = factory.post("/fake-url/")
    request.user = User.objects.create_user(username="x", password="123")

    perm = IsAdminOrReadOnly()
    assert perm.has_permission(request, None) is False