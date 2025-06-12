from rest_framework import serializers
from .models import User, Property, Availability, Booking, Wishlist, Review
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework import serializers

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'email']

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password', 'role']

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already in use.")
        return value

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = User.objects.create_user(**validated_data)
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
class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

# Reset Password
class ResetPasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_new_password = serializers.CharField(required=True)

    def validate(self, data):
        if data['new_password'] != data['confirm_new_password']:
            raise serializers.ValidationError("New passwords do not match.")
        return data

#forgot password
class ForgotpasswordSerializer(serializers.Serializer):
    otp = serializers.CharField(max_length=6)
    new_password = serializers.CharField(write_only=True, min_length=6)
    confirm_password = serializers.CharField(write_only=True, min_length=6)

    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

#send otp
class SendOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()

