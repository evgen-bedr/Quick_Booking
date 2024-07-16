# apps/core/management/commands/check_user_activity.py

from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from apps.users.models.user_model import User
from apps.rentals.models.rental_model import Rental


class Command(BaseCommand):
    help = 'Check user activity and update rental status'

    def handle(self, *args, **kwargs):
        three_months_ago = timezone.now() - timedelta(minutes=1)
        inactive_users = User.objects.filter(last_login__lt=three_months_ago, is_active=True, role='Landlord')
        for user in inactive_users:
            rentals = Rental.objects.filter(user=user)
            updated_count = rentals.update(status=False)
            user.role = 'User'
            user.save(update_fields=['role'])
