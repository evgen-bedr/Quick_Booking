from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.rentals.models.rental_model import Rental

class Command(BaseCommand):
    help = 'Update rental statuses to False if availability_end_date is past'

    def handle(self, *args, **kwargs):
        now = timezone.now().date()
        rentals = Rental.objects.filter(status=True, availability_end_date__lt=now)
        for rental in rentals:
            rental.status = False
            rental.save(update_fields=['status'])
        self.stdout.write(self.style.SUCCESS('Updated rental statuses to False where availability_end_date is past'))
