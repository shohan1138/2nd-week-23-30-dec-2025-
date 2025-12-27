from django.urls import path
from .views import FoodCategoryList, FoodItemList

urlpatterns = [
    path('categories/', FoodCategoryList.as_view(), name='category-list'),
    path('foods/', FoodItemList.as_view(), name='food-list'),
]