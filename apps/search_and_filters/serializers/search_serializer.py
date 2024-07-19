from rest_framework import serializers
from apps.search_and_filters.models.search_model import SearchHistory, UserSearchHistory


class SearchHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchHistory
        fields = ['id', 'search_query', 'created_at', 'search_count']
        read_only_fields = ['id', 'created_at', 'search_count']


class UserSearchHistorySerializer(serializers.ModelSerializer):
    search_query = serializers.CharField(source='search_history.search_query', read_only=True)

    class Meta:
        model = UserSearchHistory
        fields = ['id', 'user', 'search_query', 'created_at']
        read_only_fields = ['id', 'user', 'created_at', 'search_query']
