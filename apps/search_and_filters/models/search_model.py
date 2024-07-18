# apps/search_and_filters/models/search_model.py
from django.db import models
from django.conf import settings

class SearchHistory(models.Model):
    search_query = models.CharField(max_length=255, unique=True)
    search_count = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.search_query} - {self.search_count}"

class UserSearchHistory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    search_history = models.ForeignKey(SearchHistory, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.search_history.search_query}"
