# apps/search_and_filters/models/search_model.py
from django.db import models
from django.conf import settings


class SearchHistory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    search_query = models.CharField(max_length=255)  # Увеличим длину поля для сохранения длинных запросов
    created_at = models.DateTimeField(auto_now_add=True)
    search_count = models.IntegerField(default=1)

    class Meta:
        unique_together = ('user', 'search_query')

    def __str__(self):
        return f"{self.user.username} - {self.search_query} - {self.search_count}"
