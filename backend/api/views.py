from rest_framework import generics
from .models import FoodCategory, FoodItem
from .serializers import FoodCategorySerializer, FoodItemSerializer
from rest_framework.permissions import AllowAny


class FoodCategoryList(generics.ListCreateAPIView):
    queryset = FoodCategory.objects.all()
    serializer_class = FoodCategorySerializer
    permission_classes = [AllowAny]
    
class FoodItemList(generics.ListCreateAPIView):
    queryset = FoodItem.objects.all()
    serializer_class = FoodItemSerializer
    permission_classes = [AllowAny]