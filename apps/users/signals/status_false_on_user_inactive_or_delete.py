from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from apps.users.models.user_model import User
from apps.rentals.models.rental_model import Rental


@receiver(post_delete, sender=User)
def set_rental_status_false_on_user_delete(sender, instance, **kwargs):
    rentals = Rental.objects.filter(user=instance)
    rentals.update(status=False)


@receiver(post_save, sender=User)
def set_rental_status_false_on_user_inactive(sender, instance, **kwargs):
    if not instance.is_active:
        rentals = Rental.objects.filter(user=instance)
        rentals.update(status=False)
