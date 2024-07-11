from django.shortcuts import get_object_or_404
from django.http import HttpResponse

from apps.rentals.models.rental_model import Rental


def view_rental(request, rental_id):
    rental = get_object_or_404(Rental, id=rental_id)
    rental.increment_views()
    return HttpResponse(f"This rental has been viewed {rental.views_count} times.")
