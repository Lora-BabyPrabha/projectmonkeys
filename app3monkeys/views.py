from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Q
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model

from .models import Property, Booking, Availability, Wishlist, Review
from .serializers import (
    PropertySerializer, BookingSerializer, AvailabilitySerializer,
    WishlistSerializer, ReviewSerializer, UserSerializer, RegisterSerializer, UserListSerializer
)
from .permissions import IsVendor, IsCustomer, IsOwnerOrReadOnly

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


# Property View
class PropertyViewSet(viewsets.ModelViewSet):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(vendor=self.request.user)

    def get_queryset(self):
        queryset = Property.objects.all()
        q = self.request.query_params.get('q')
        if q:
            queryset = queryset.filter(
                Q(title__icontains=q) |
                Q(location__icontains=q) |
                Q(description__icontains=q)
            )
        return queryset


# Availability View
class AvailabilityViewSet(viewsets.ModelViewSet):
    queryset = Availability.objects.all()
    serializer_class = AvailabilitySerializer
    permission_classes = [permissions.IsAuthenticated, IsVendor]


# Booking View
class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated, IsCustomer]

    def perform_create(self, serializer):
        prop = serializer.validated_data['property']
        nights = (serializer.validated_data['check_out'] - serializer.validated_data['check_in']).days
        total_price = nights * prop.price_per_night
        serializer.save(customer=self.request.user, total_price=total_price)


# Wishlist View
class WishlistViewSet(viewsets.ModelViewSet):
    queryset = Wishlist.objects.all()
    serializer_class = WishlistSerializer
    permission_classes = [permissions.IsAuthenticated, IsCustomer]

    def get_queryset(self):
        return Wishlist.objects.filter(customer=self.request.user)

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)


# Review View
class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated, IsCustomer]

    def get_queryset(self):
        return Review.objects.filter(customer=self.request.user)

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)


# User List View
class UserListViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    permission_classes = [permissions.AllowAny]
