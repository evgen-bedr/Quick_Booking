from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.search_and_filters.views.search_history_view import SearchHistoryViewSet
from apps.search_and_filters.views.search_view import SearchViewSet

router = DefaultRouter()
router.register(r'search-history', SearchHistoryViewSet, basename='search-history')
router.register(r'search', SearchViewSet, basename='search')

urlpatterns = [
    path('', include(router.urls)),
]
