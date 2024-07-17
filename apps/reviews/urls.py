from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.reviews.views.review_view import ReviewViewSet

router = DefaultRouter()
router.register(r'rentals/(?P<rental_id>\d+)/reviews', ReviewViewSet, basename='rental-reviews')

# urlpatterns = [
#     path('', include(router.urls)),
#     path('create/', ReviewViewSet.as_view({'post': 'perform_create'}), name='review-create'),
#     path('<int:id>/', ReviewViewSet.as_view({'get': 'retrieve'}), name='review-detail'),
#     path('update/<int:id>/', ReviewViewSet.as_view({'put': 'perform_update', 'patch': 'partial_update'}),
#          name='review-update'),
#     path('delete/<int:id>/', ReviewViewSet.as_view({'delete': 'destroy'}), name='review-delete'),
# ]

urlpatterns = [
    path('', include(router.urls)),
    # path('<int:pk>/', ReviewViewSet.as_view({'get': 'retrieve'}), name='review-detail'),
    # path('reviews/rental/<int:rental_id>/create/', ReviewViewSet.as_view({'post': 'create'}),
    #      name='review-create'),
    # path('create/', ReviewViewSet.as_view({'post': 'create'}), name='review-create'),
    # path('reviews/rentals/<int:rental_id>/', ReviewViewSet.as_view({'get': 'list'}), name='review-list'),
    # path('<int:pk>/update/', ReviewViewSet.as_view({'put': 'perform_update', 'patch': 'partial_update'}),
    #      name='review-update'),
    # path('<int:pk>/delete/', ReviewViewSet.as_view({'delete': 'destroy'}), name='review-delete'),
]
