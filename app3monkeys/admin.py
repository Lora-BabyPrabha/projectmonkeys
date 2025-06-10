from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import User, Property, Booking, Availability, Wishlist, Review
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


class CustomUserAdmin(BaseUserAdmin):
    model = User
    list_display = ['username', 'email', 'role']
    fieldsets = BaseUserAdmin.fieldsets + (
        (None, {'fields': ('role', 'phone')}),
    )


admin.site.register(User, CustomUserAdmin)
admin.site.register(Property)
admin.site.register(Booking)
admin.site.register(Availability)
admin.site.register(Wishlist)
admin.site.register(Review)
