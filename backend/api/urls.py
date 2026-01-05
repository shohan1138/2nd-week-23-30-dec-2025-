
from django.urls import path
from .views import FoodCategoryDetail, FoodCategoryList, FoodItemList, MealPlanList, OrderList, OrderItemList, ordercancel, orderdetail, orderstatusupdate, VerifyOTPView, LoginView, payorder


urlpatterns = [
    path("verify-otp/", VerifyOTPView.as_view(), name="verify-otp"),
    path("login/", LoginView.as_view(), name="login"),

    path('categories/', FoodCategoryList.as_view(), name='foodcategory-list'),
    path('categories/<int:pk>/', FoodCategoryDetail.as_view(), name='foodcategory-detail'),

    path('foods/', FoodItemList.as_view(), name='fooditem-list'),
    path('foods/<int:pk>/', FoodItemList.as_view(), name='fooditem-detail'),
    path('mealplans/', MealPlanList.as_view(), name='mealplan-list'),
    path('mealplans/<int:pk>/', MealPlanList.as_view(), name='mealplan-detail'),

    path('orders/', OrderList.as_view(),name='order-list'),
    path('orders/<int:pk>/', OrderList.as_view(), name='order-detail'),

    path('order-items/', OrderItemList.as_view()),
    path('order-items/<int:pk>/', OrderItemList.as_view()),
    path('orders/<int:pk>/status/', orderstatusupdate.as_view()),
    path('orders/<int:pk>/cancel/', ordercancel.as_view()),
    path('orders/<int:pk>/', orderdetail.as_view()),
    path('orders/<int:pk>/pay/', payorder.as_view()),
]

