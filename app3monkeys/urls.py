from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PropertyViewSet, BookingViewSet, AvailabilityViewSet,
    WishlistViewSet, ReviewViewSet, RegisterViewSet, CustomTokenObtainPairView
)
from rest_framework_simplejwt.views import TokenRefreshView
 
router = DefaultRouter()
router.register(r'properties', PropertyViewSet)
router.register(r'availability', AvailabilityViewSet)
router.register(r'bookings', BookingViewSet)
router.register(r'wishlist', WishlistViewSet, basename='wishlist')
router.register(r'reviews', ReviewViewSet, basename='reviews')
router.register(r'register', RegisterViewSet, basename='register')  # Handles signup via POST
 
urlpatterns = [
    path('api/', include(router.urls)),
 
    # JWT Authentication endpoints
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),  # login
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),       # refresh token
]