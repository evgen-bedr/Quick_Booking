from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from apps.rentals.models.rental_model import Rental


@receiver(post_save, sender=Rental)
def update_user_role_on_save(sender, instance, **kwargs):
    instance.update_user_role()


@receiver(post_delete, sender=Rental)
def update_user_role_on_delete(sender, instance, **kwargs):
    instance.update_user_role()
