from rest_framework import serializers
from .models import FoodCategory,FoodItem,MealPlan,Order,OrderItem

class FoodCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodCategory
        fields = "__all__"
class FoodItemSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=FoodCategory.objects.all())
    class Meta:
        model = FoodItem
        fields = "__all__"

class MealPlanSerializer(serializers.ModelSerializer):
    foods = FoodItemSerializer(many=True, read_only=True)
    class Meta:
        model = MealPlan
        fields = "__all__"
class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = "__all__"

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Quantity must be greater than 0")
        return value
    def validate(self, attrs):
        food=attrs['food']
        if not food.is_available:
            raise serializers.ValidationError("This food item is not available")
        return attrs
class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    class Meta:
        model = Order
        fields = "__all__"