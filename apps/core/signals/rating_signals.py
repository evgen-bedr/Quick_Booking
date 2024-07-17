from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from apps.reviews.models.review_model import Review
from apps.core.utils.rating_utils import update_rating_and_reviews


@receiver(post_save, sender=Review)
def update_rental_on_save(sender, instance, **kwargs):
    update_rating_and_reviews(instance.rental)


@receiver(post_delete, sender=Review)
def update_rental_on_delete(sender, instance, **kwargs):
    update_rating_and_reviews(instance.rental)
