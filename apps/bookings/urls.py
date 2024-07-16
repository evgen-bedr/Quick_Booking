from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.bookings.views.cancel_booking_view import CancelBookingView
from apps.bookings.views.confirm_booking_view import ConfirmBookingView
from apps.bookings.views.create_booking_view import CreateBookingView
from apps.bookings.views.landlord_booking_list_view import LandlordBookingListView
from apps.bookings.views.user_booking_list_view import UserBookingListView

router = DefaultRouter()

router = DefaultRouter()
router.register(r'create', CreateBookingView, basename='create-booking')
router.register(r'list', UserBookingListView, basename='user-bookings')
router.register(r'landlord-list', LandlordBookingListView, basename='landlord-bookings')

urlpatterns = [
    path('cancel/<int:pk>/', CancelBookingView.as_view({'post': 'update'}), name='cancel-booking'),
    path('confirm/<int:pk>/', ConfirmBookingView.as_view({'post': 'update'}), name='confirm-booking'),
    path('', include(router.urls)),
]