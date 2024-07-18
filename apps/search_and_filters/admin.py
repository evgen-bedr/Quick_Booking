# apps/search_and_filters/admin.py
from django.contrib import admin
from apps.search_and_filters.models.search_model import SearchHistory, UserSearchHistory

class SearchHistoryAdmin(admin.ModelAdmin):
    list_display = ('search_query', 'search_count', 'created_at')
    search_fields = ('search_query',)
    ordering = ('-search_count',)  # Сортировка по умолчанию по убыванию search_count

admin.site.register(SearchHistory, SearchHistoryAdmin)

class UserSearchHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'search_history', 'created_at')
    list_filter = ('user', 'created_at')
    search_fields = ('user__username', 'search_history__search_query')
    readonly_fields = ('created_at',)

admin.site.register(UserSearchHistory, UserSearchHistoryAdmin)
