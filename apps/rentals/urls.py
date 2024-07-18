# apps/rental/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.rentals.views.rental_admin_view import RentalAdminViewSet
from apps.rentals.views.rental_view import RentalViewSet
from apps.rentals.views.pending_rental_view import (
    PendingRentalViewSet,
    pending_rentals_view,
    pending_rentals_data,
    pending_rentals_list,
    approve_rental,
    reject_rental
)

router = DefaultRouter()
router.register(r'', RentalViewSet, basename='rental')
router.register(r'admin/rentals', RentalAdminViewSet, basename='admin-rental')
router.register(r'admin/pending-rentals', PendingRentalViewSet, basename='pending-rental')

urlpatterns = [
    path('admin/pending-rentals/data/', pending_rentals_data, name='pending_rentals_data'),
    path('admin/pending-rentals/list/', pending_rentals_list, name='pending_rentals_list'),
    path('admin/pending-rentals/html/', pending_rentals_view, name='pending_rentals'),
    path('admin/pending-rentals/approve/<int:rental_id>/', approve_rental, name='approve_rental'),
    path('admin/pending-rentals/reject/<int:rental_id>/', reject_rental, name='reject_rental'),
    path('', include(router.urls)),
]
