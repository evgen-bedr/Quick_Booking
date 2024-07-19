from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.reviews.views.review_view import ReviewViewSet
from apps.reviews.views.pending_review_view import (
    PendingReviewViewSet,
    pending_reviews_view,
    pending_reviews_list,
    approve_review,
    reject_review
)
from apps.reviews.views.user_reviews_view import UserReviewsViewSet

router = DefaultRouter()
router.register(r'rentals/(?P<rental_id>\d+)', ReviewViewSet, basename='reviews')
router.register(r'admin/pending-reviews', PendingReviewViewSet, basename='pending-reviews')
router.register(r'user-reviews', UserReviewsViewSet, basename='user-reviews')

urlpatterns = [
    path('admin/pending-reviews/list/', pending_reviews_list, name='pending_reviews_list'),
    path('admin/pending-reviews/html/', pending_reviews_view, name='pending_reviews'),
    path('admin/pending-reviews/approve/<int:review_id>/', approve_review, name='approve_review'),
    path('admin/pending-reviews/reject/<int:review_id>/', reject_review, name='reject_review'),
    path('', include(router.urls)),
]
