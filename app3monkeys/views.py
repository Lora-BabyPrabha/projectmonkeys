from django.shortcuts import render
from rest_framework import generics
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Q
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.hashers import check_password
from rest_framework.permissions import IsAuthenticated
from .serializers import ResetPasswordSerializer
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from .serializers import ForgotpasswordSerializer
from .models import Property, Booking, Availability, Wishlist, Review
from .serializers import (
    PropertySerializer, BookingSerializer, AvailabilitySerializer,
    WishlistSerializer, ReviewSerializer, UserSerializer, RegisterSerializer, UserListSerializer, ForgotpasswordSerializer, SendOTPSerializer
)
from .permissions import  IsAdmin, IsUser
from rest_framework.generics import GenericAPIView

User = get_user_model()


# Auth views
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        user_data = UserSerializer(self.user).data
        data['user'] = user_data
        data['role'] = self.user.role  # ✅ Include role
        return data

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class RegisterViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()  # ✅ Required for ModelViewSet
    serializer_class = RegisterSerializer
    http_method_names = ['post']
    permission_classes = [permissions.AllowAny]  # ✅ Allow public access to register


from .permissions import IsAdminOrReadOnlyForUser
from rest_framework import permissions

class PropertyViewSet(viewsets.ModelViewSet):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrReadOnlyForUser]

# Availability View
from .permissions import IsAdminOrReadOnlyForUser

class AvailabilityViewSet(viewsets.ModelViewSet):
    queryset = Availability.objects.all()
    serializer_class = AvailabilitySerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrReadOnlyForUser]

# Booking View
from .permissions import IsBookingOwnerOrAdminReadOnly

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()  # Add this line back!
    serializer_class = BookingSerializer
    permission_classes = [IsBookingOwnerOrAdminReadOnly]
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'Admin':
            return Booking.objects.all()
        return Booking.objects.filter(customer=user)


# Wishlist View
class WishlistViewSet(viewsets.ModelViewSet):
    queryset = Wishlist.objects.all()
    serializer_class = WishlistSerializer
    permission_classes = [permissions.IsAuthenticated, IsUser]

    def get_queryset(self):
        return Wishlist.objects.filter(customer=self.request.user)

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)


# Review View
from .permissions import IsReviewOwnerOrAdminReadOnly

class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsReviewOwnerOrAdminReadOnly]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'Admin':
            return Review.objects.all()  # Admin sees all reviews
        return Review.objects.filter(customer=user)  # User sees only their own

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)


# User List View
class UserListViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]


#Reset password
class ResetPasswordView(generics.UpdateAPIView):
    serializer_class = ResetPasswordSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            user = request.user  # Use the authenticated user
            old_password = serializer.validated_data['old_password']
            new_password = serializer.validated_data['new_password']

            if not user.check_password(old_password):
                return Response(
                    {"old_password": "Incorrect old password."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            user.set_password(new_password)
            user.save()
            return Response(
                {"detail": "Password updated successfully."},
                status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Forgot Password
class ForgotpasswordView(GenericAPIView):
    serializer_class = ForgotpasswordSerializer

    def get(self, request):
        return Response(self.get_serializer().data)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']  # ✅ Fix: extract email from validated_data
            otp = serializer.validated_data['otp']
            new_password = serializer.validated_data['new_password']

            if OTP_STORE.get(email) != otp:
                return Response({"error": "Invalid OTP"}, status=400)

            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({"error": "User not found"}, status=404)

            user.set_password(new_password)
            user.save()
            OTP_STORE.pop(email, None)

            return Response({"message": "Password reset successfully."})
        return Response(serializer.errors, status=400)


OTP_STORE = {}
# Send OTP
class SendOTPView(GenericAPIView):
    serializer_class = SendOTPSerializer

    def get(self, request):
        # Return empty form fields in HTML
        return Response(self.get_serializer().data)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({"error": "User not found"}, status=404)

            otp = get_random_string(length=6, allowed_chars='0123456789')
            OTP_STORE[email] = otp  # In-memory for demo

            send_mail(
                subject='Your OTP Code',
                message=f'Your OTP is: {otp}',
                from_email='noreply@3monkeys.com',
                recipient_list=[email],
                fail_silently=False,
            )

            return Response({"message": "OTP sent to your email."}, status=200)

        return Response(serializer.errors, status=400)
