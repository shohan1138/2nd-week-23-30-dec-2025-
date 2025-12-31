from django.contrib import admin
from .models import FoodCategory, FoodItem, MealPlan, Order, OrderItem   

@admin.register(FoodCategory)
class FoodCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(FoodItem)
class FoodItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'price', 'is_available')
    list_filter = ('category', 'is_available')
    search_fields = ('name',)


@admin.register(MealPlan)
class MealPlanAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'user', 'created_at')
    filter_horizontal = ('foods',)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_price', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username',)
    inlines = [OrderItemInline]

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'food', 'quantity', 'price')
