from django.contrib.auth.models import User
from django.core.mail import send_mail
import random
from rest_framework import serializers
from .models import FoodCategory,FoodItem,MealPlan,Order,OrderItem,EmailOTP

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
    foods = serializers.PrimaryKeyRelatedField(
        queryset=FoodItem.objects.all(),
        many=True
    )

    class Meta:
        model = MealPlan
        fields = ['id', 'title', 'foods', 'created_at']
class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'food', 'quantity', 'price']
        read_only_fields = ['price']



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
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Order
        fields = ['id', 'user', 'total_price', 'status', 'items']
        read_only_fields = ['id', 'user', 'total_price', 'status', 'items']

class UserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'confirm_password']    
        extra_kwargs = {'password': {'write_only': True}}   
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email is already in use.")
        return value
    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        return data
    def create(self, validated_data):
        validated_data.pop('confirm_password')
        User.objects.filter(email=validated_data['email'], is_active=False).delete()
        user =User.objects.create_user(**validated_data)
        user.is_active = False
        user.save()
        return user

class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
