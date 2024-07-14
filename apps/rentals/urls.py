from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.rentals.views.rental_admin_view import RentalAdminViewSet
from apps.rentals.views.rental_view import RentalViewSet
from apps.rentals.views.pending_rental_view import (
    PendingRentalViewSet,
    pending_rentals_view,
    pending_rentals_data,
    pending_rentals_list,
    approve_rental
)

router = DefaultRouter()
router.register(r'rentals', RentalViewSet, basename='rental')
router.register(r'admin/rentals', RentalAdminViewSet, basename='admin-rental')
router.register(r'admin/pending-rentals', PendingRentalViewSet, basename='pending-rental')

urlpatterns = [
    # Отдельные маршруты для функций представлений (FBV)
    path('admin/pending-rentals/data/', pending_rentals_data, name='pending_rentals_data'),
    path('admin/pending-rentals/list/', pending_rentals_list, name='pending_rentals_list'),
    path('admin/pending-rentals/', pending_rentals_view, name='pending_rentals'),
    path('admin/pending-rentals/approve/<int:rental_id>/', approve_rental, name='approve_rental'),

    # Маршруты, зарегистрированные с помощью DefaultRouter
    path('', include(router.urls)),
    path('rental/', RentalViewSet.as_view({'get': 'list'}), name='rental-list'),
    path('rental/<int:id>/', RentalViewSet.as_view({'get': 'retrieve'}), name='rental-detail'),
    path('rental/create/', RentalViewSet.as_view({'post': 'create'}), name='rental-create'),
    path('rental/update/<int:id>/', RentalViewSet.as_view({'put': 'update', 'patch': 'partial_update'}), name='rental-update'),
    path('rental/delete/<int:id>/', RentalViewSet.as_view({'delete': 'destroy'}), name='rental-delete'),
    path('rental/remove_images/<int:id>/', RentalViewSet.as_view({'delete': 'remove_images'}), name='rental-remove-images'),

]
