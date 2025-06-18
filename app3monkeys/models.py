from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.db import models
from multiselectfield import MultiSelectField


class User(AbstractUser):
    ROLE_CHOICES = (
        ('User', 'User'),
        ('Admin', 'Admin'),
    )
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    def __str__(self):
        return self.username

# Property Listing
CHECKLIST_CHOICES = (
    ('wifi', 'WiFi'),
    ('pool', 'Pool'),
    ('parking', 'Parking'),
    ('pet_friendly', 'Pet Friendly'),
)

class Property(models.Model):
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=100, default="General")
    location = models.CharField(max_length=255, default="Unknown")
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    guestLimit = models.IntegerField()
    image = models.URLField(max_length=500, blank=True, null=True)
    aminities = MultiSelectField(choices=CHECKLIST_CHOICES, blank=True)

    def __str__(self):
        return self.title

# Availability Calendar
class Availability(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='availability')
    date = models.DateField()
    is_available = models.BooleanField(default=True)

    class Meta:
        unique_together = ('property', 'date')

    def __str__(self):
        return f"{self.property.title} - {self.date} - {self.is_available}"


# Booking Model
class Booking(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='bookings')
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    check_in = models.DateField()
    check_out = models.DateField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer.username} booking at {self.property.title}"


# Wishlist Model
class Wishlist(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlist')
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='wishlisted_by')
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('customer', 'property')


# Review Model
class Review(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='reviews')
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('property', 'customer')

    def __str__(self):
        return f"{self.customer.username} - {self.property.title} - {self.rating}"
from django.db import models
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()

class PasswordResetOTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"OTP for {self.user.email} - {self.otp}"
 