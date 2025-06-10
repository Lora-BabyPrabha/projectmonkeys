from rest_framework import serializers
from .models import User, Property, Availability, Booking, Wishlist, Review
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password


# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'email', 'phone', 'role']


# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'password', 'password2', 'role', 'phone']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Passwords didn’t match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = get_user_model().objects.create_user(**validated_data)
        return user


# Property Serializer
class PropertySerializer(serializers.ModelSerializer):
    vendor = UserSerializer(read_only=True)

    class Meta:
        model = Property
        fields = '__all__'
        read_only_fields = ['vendor', 'created_at']


# Availability Serializer
class AvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Availability
        fields = ['id', 'property', 'date', 'is_available']


# Booking Serializer
class BookingSerializer(serializers.ModelSerializer):
    customer = UserSerializer(read_only=True)
    property = PropertySerializer(read_only=True)
    property_id = serializers.PrimaryKeyRelatedField(queryset=Property.objects.all(), write_only=True, source='property')

    class Meta:
        model = Booking
        fields = ['id', 'property', 'property_id', 'customer', 'check_in', 'check_out', 'total_price', 'is_paid', 'created_at']
        read_only_fields = ['customer', 'total_price', 'is_paid', 'created_at']


# Wishlist Serializer
class WishlistSerializer(serializers.ModelSerializer):
    property = PropertySerializer(read_only=True)
    property_id = serializers.PrimaryKeyRelatedField(queryset=Property.objects.all(), source='property', write_only=True)

    class Meta:
        model = Wishlist
        fields = ['id', 'customer', 'property', 'property_id', 'added_at']
        read_only_fields = ['customer', 'added_at']


# Review Serializer
class ReviewSerializer(serializers.ModelSerializer):
    customer = UserSerializer(read_only=True)
    property = PropertySerializer(read_only=True)
    property_id = serializers.PrimaryKeyRelatedField(queryset=Property.objects.all(), source='property', write_only=True)

    class Meta:
        model = Review
        fields = ['id', 'property', 'property_id', 'customer', 'rating', 'comment', 'created_at']
        read_only_fields = ['customer', 'created_at']
