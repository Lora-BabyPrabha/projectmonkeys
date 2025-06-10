from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PropertyViewSet, BookingViewSet, AvailabilityViewSet,
    WishlistViewSet, ReviewViewSet, RegisterViewSet, CustomTokenObtainPairView
)

router = DefaultRouter()
router.register(r'properties', PropertyViewSet)
router.register(r'availability', AvailabilityViewSet)
router.register(r'bookings', BookingViewSet)
router.register(r'wishlist', WishlistViewSet, basename='wishlist')
router.register(r'reviews', ReviewViewSet, basename='reviews')
router.register(r'register', RegisterViewSet, basename='register')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
]
