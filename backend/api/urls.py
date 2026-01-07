
from django.urls import path
from .views import FoodCategoryDetail, FoodCategoryList, FoodItemList, MealPlanList, OrderList, OrderItemList, ordercancel, orderdetail, orderstatusupdate, VerifyOTPView, LoginView, payorder


urlpatterns = [
    path('categories/', FoodCategoryList.as_view()),
    path('categories/<int:pk>/', FoodCategoryDetail.as_view()),

    path('foods/', FoodItemList.as_view()),
    path('foods/<int:pk>/', FoodItemList.as_view()),

    path('mealplans/', MealPlanList.as_view()),
    path('mealplans/<int:pk>/', MealPlanList.as_view()),

    path('orders/', OrderList.as_view()),
    path('orders/<int:pk>/', orderdetail.as_view(), name='order-detail'),
    
    path('orders/<int:pk>/status/', orderstatusupdate.as_view()),
    path('orders/<int:pk>/cancel/', ordercancel.as_view()),
    path('orders/<int:pk>/pay/', payorder.as_view()),

    path('order-items/', OrderItemList.as_view()),
    path('order-items/<int:pk>/', OrderItemList.as_view()),
]