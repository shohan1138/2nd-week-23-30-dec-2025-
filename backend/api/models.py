from django.db import models
from django.contrib.auth.models import User

class FoodCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class FoodItem(models.Model):
    category=models.ForeignKey(FoodCategory, related_name='foods', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    calories = models.PositiveIntegerField()
    protein = models.FloatField()
    carbs = models.FloatField()
    fats = models.FloatField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    is_available = models.BooleanField(default=True)

    class Meta:
        unique_together = ('category', 'name')
    
    def __str__(self):
        return self.name
class MealPlan(models.Model):
    user = models.ForeignKey(User, related_name='MealPlans', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    foods=models.ManyToManyField(FoodItem)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
class Order(models.Model):
    user =models.ForeignKey(User, related_name='Orders', on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(
        max_length=50, 
        choices=[
            ('pending', 'Pending'), 
            ('paid', 'Paid'),
            ('canceled', 'Canceled')
        ], 
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id}"
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    food = models.ForeignKey(FoodItem, related_name='order_items', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.food.name}"