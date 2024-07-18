# apps/bookings/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.bookings.views.booked_dates_view import BookedDatesViewSet
from apps.bookings.views.booking_view import BookingViewSet
from apps.bookings.views.landlord_confirm_booking_view import LandlordConfirmBookingViewSet

router = DefaultRouter()
router.register(r'landlord', LandlordConfirmBookingViewSet, basename='landlord-bookings')
router.register(r'', BookingViewSet, basename='bookings')

urlpatterns = [
    path('', include(router.urls)),
    path('dates/<int:rental_id>/', BookedDatesViewSet.as_view({'get': 'list'}), name='bookings-dates'),

]
