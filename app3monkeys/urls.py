from django.urls import path, include
from .views import UserListViewSet
from .views import SendOTPView, PasswordResetAllInOneView
from rest_framework.routers import DefaultRouter
from .views import UserListViewSet
from .views import (
    PropertyViewSet, BookingViewSet, AvailabilityViewSet,
    WishlistViewSet, ReviewViewSet, RegisterViewSet, CustomTokenObtainPairView, ResetPasswordView
)
from rest_framework_simplejwt.views import TokenRefreshView
 
router = DefaultRouter()
router.register(r'properties', PropertyViewSet)
router.register(r'availability', AvailabilityViewSet)
router.register(r'bookings', BookingViewSet)
router.register(r'wishlist', WishlistViewSet, basename='wishlist')
router.register(r'reviews', ReviewViewSet, basename='reviews')
router.register(r'register', RegisterViewSet, basename='register')
router.register(r'users', UserListViewSet, basename='userlist')  # Handles signup via POST
urlpatterns = [
    path('api/', include(router.urls)),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),  # login
    path('api/Reset-password/', ResetPasswordView.as_view(), name='Reset-password'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), 
    path('send-otp/', SendOTPView.as_view(), name='send-otp'),
    path('new-password/', PasswordResetAllInOneView.as_view(), name='new-password'),     # refresh token

]