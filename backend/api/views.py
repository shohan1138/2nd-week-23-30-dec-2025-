from rest_framework import generics
from .models import FoodCategory, FoodItem, MealPlan, Order, OrderItem, EmailOTP
from .serializers import FoodCategorySerializer, FoodItemSerializer,MealPlanSerializer, OrderSerializer, OrderItemSerializer, UserSerializer, VerifyOTPSerializer, LoginSerializer
from rest_framework.permissions import AllowAny,IsAuthenticated, IsAdminUser
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import SAFE_METHODS
from django.shortcuts import render
from django.utils import timezone
from django.conf import settings
import random
from django.core.mail import send_mail
from api.models import EmailOTP



class ISAdminOrReadOnly(IsAdminUser):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_staff
class FoodCategoryList(generics.ListCreateAPIView):
    queryset = FoodCategory.objects.all().order_by('id')
    serializer_class = FoodCategorySerializer
    permission_classes = [AllowAny]


class FoodCategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = FoodCategory.objects.all()
    serializer_class = FoodCategorySerializer
    permission_classes = [AllowAny]

class FoodItemList(generics.ListCreateAPIView):
    queryset = FoodItem.objects.all().order_by('id')
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
        if order.status not in ["paid","canceled"]:
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


class createUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        otp = str(random.randint(100000, 999999))
        EmailOTP.objects.create(
            user=user,
            otp_code=otp,
        )
        send_mail(
        subject="Your OTP Verification Code",
        message=f"Your OTP is {otp}. It will expire in 2 minutes.",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user.email],
        fail_silently=False,
        )

        print("OTP:", otp)
class VerifyOTPView(APIView):
    permission_classes = [AllowAny]
    serializer_class = VerifyOTPSerializer

    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data['email']
            otp_code = serializer.validated_data['otp']

            try:
                user = User.objects.get(email=email)
                otp_entry = EmailOTP.objects.get(user=user, otp_code=otp_code, is_used=False)

                if otp_entry.expires_at < timezone.now():
                    return Response({"detail": "OTP has expired."}, status=status.HTTP_400_BAD_REQUEST)

                otp_entry.is_used = True
                otp_entry.save()

                user.is_active = True
                user.save()

                return Response({"detail": "OTP verified successfully."}, status=status.HTTP_200_OK)

            except User.DoesNotExist:
                return Response({"detail": "User with this email does not exist."}, status=status.HTTP_400_BAD_REQUEST)
            except EmailOTP.DoesNotExist:
                return Response({"detail": "Invalid OTP."}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class LoginView(APIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {"detail": "Invalid credentials."},
                status=status.HTTP_401_UNAUTHORIZED
            )

        if not EmailOTP.objects.filter(user=user, is_used=True).exists():
            return Response(
                {"detail": "Account not verified."},
                status=status.HTTP_403_FORBIDDEN
            )

        user = authenticate(username=user.username, password=password)
        if not user:
            return Response(
                {"detail": "Invalid credentials."},
                status=status.HTTP_401_UNAUTHORIZED
            )

        refresh = RefreshToken.for_user(user)

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })
class payorder(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        try:
            order = Order.objects.get(pk=pk, user=request.user)
        except Order.DoesNotExist:
            return Response({"detail": "Order not found."}, status=status.HTTP_404_NOT_FOUND)

        if order.status == 'paid':
            return Response({"detail": "Order is already paid."}, status=status.HTTP_400_BAD_REQUEST)

        order.status = 'paid'
        order.save()
        return Response({"detail": "Order marked as paid."}, status=status.HTTP_200_OK)