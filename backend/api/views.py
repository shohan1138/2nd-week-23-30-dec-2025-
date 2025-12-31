from rest_framework import generics
from .models import FoodCategory, FoodItem, MealPlan, Order, OrderItem
from .serializers import FoodCategorySerializer, FoodItemSerializer,MealPlanSerializer, OrderSerializer, OrderItemSerializer
from rest_framework.permissions import AllowAny,IsAuthenticated, IsAdminUser
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import SAFE_METHODS

class ISAdminOrReadOnly(IsAdminUser):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_staff
class FoodCategoryList(generics.RetrieveUpdateDestroyAPIView):
    queryset = FoodCategory.objects.all()
    serializer_class = FoodCategorySerializer
    permission_classes = [AllowAny]


class FoodItemList(generics.ListCreateAPIView):
    queryset = FoodItem.objects.all()
    serializer_class = FoodItemSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdminUser()]
        return [AllowAny()]


class MealPlanList(generics.RetrieveUpdateDestroyAPIView):
    queryset = MealPlan.objects.all()
    serializer_class = MealPlanSerializer
    permission_classes = [AllowAny]

class OrderList(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user= self.request.user
        if user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(user=user)

    def perform_create(self, serializer):
        order = serializer.save(user=self.request.user)
        total = sum(
            item.food.price * item.quantity
            for item in order.items.all()
        )
        order.total_price = total
        order.save()


class OrderItemList(generics.ListCreateAPIView):
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return OrderItem.objects.filter(order__user=self.request.user)

    def perform_create(self, serializer):
        food = serializer.validated_data['food']
        quantity = serializer.validated_data['quantity']
        price = food.price * quantity

        serializer.save(price=price)

class orderstatusupdate(APIView):
    permission_classes = [IsAdminUser]

    def patch(self, request, pk):
        try:
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return Response({"error": "Order not found."}, status=status.HTTP_404_NOT_FOUND)

        order.status = request.data.get('status', order.status)
        if order.status not in ["paid","cacelled"]:
            return Response({"error": "Invalid status."}, status=status.HTTP_400_BAD_REQUEST)
        order.save()
        return Response({"detail": "Order status updated."}, status=status.HTTP_200_OK)
       
    
class ordercancel(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        try:
            order = Order.objects.get(pk=pk, user=request.user)
        except Order.DoesNotExist:
            return Response({"detail": "Order not found."}, status=status.HTTP_404_NOT_FOUND)

        if order.status == 'canceled':
            return Response({"detail": "Order is already canceled."}, status=status.HTTP_400_BAD_REQUEST)

        order.status = 'canceled'
        order.save()
        return Response({"detail": "Order canceled."}, status=status.HTTP_200_OK)
    
class orderdetail(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        order = super().get_object()
        if self.request.user.is_staff or order.user == self.request.user:
            return order
        else:
            raise PermissionDenied("You do not have permission to view this order.")