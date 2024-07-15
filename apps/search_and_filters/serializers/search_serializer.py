# apps/search_and_filters/serializers/search_serializer.py
from rest_framework import serializers
from apps.search_and_filters.models.search_model import SearchHistory

class SearchHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchHistory
        fields = ['id', 'user', 'search_query', 'created_at', 'search_count']
        read_only_fields = ['id', 'user', 'created_at', 'search_count']
