from django.contrib import admin
from .model import FoodCategory, FoodItem, MealPlan, Order, OrderItem   

admin.site.register(FoodCategory)
admin.site.register(FoodItem)
admin.site.register(MealPlan)
admin.site.register(Order)
admin.site.register(OrderItem)


