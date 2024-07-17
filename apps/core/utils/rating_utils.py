from django.db.models import Sum
from apps.reviews.models.review_model import Review


def update_rating_and_reviews(rental):
    reviews_with_ratings = Review.objects.filter(rental=rental).exclude(rating__isnull=True)
    reviews_with_comments = Review.objects.filter(rental=rental).exclude(comment__isnull=True).exclude(
        comment__exact='')

    rental.ratings_count = reviews_with_ratings.count()
    rental.ratings_sum = reviews_with_ratings.aggregate(Sum('rating'))['rating__sum'] or 0
    rental.reviews_count = reviews_with_comments.count()
    rental.save(update_fields=['ratings_sum', 'ratings_count', 'reviews_count'])
