from django.http import JsonResponse
from rest_framework import viewsets
from apps.rentals.models.rental_model import Rental
from apps.rentals.serializers.rental_serializer import RentalSerializer
from django.shortcuts import render, redirect
from apps.rentals.decorators.moderator_decorator import moderator_required
from apps.core.permissions.authenticated_user_moder_superuser import IsModeratorOrAdmin

class PendingRentalViewSet(viewsets.ModelViewSet):
    queryset = Rental.objects.filter(verified=False)
    serializer_class = RentalSerializer
    permission_classes = [IsModeratorOrAdmin]

@moderator_required
def pending_rentals_view(request):
    rentals = Rental.objects.filter(verified=False)
    return render(request, 'pending_rentals.html', {'rentals': rentals})

@moderator_required
def pending_rentals_data(request):
    rentals = Rental.objects.filter(verified=False).values('id', 'title', 'description')
    return JsonResponse(list(rentals), safe=False)

@moderator_required
def pending_rentals_list(request):
    rentals = Rental.objects.filter(verified=False)
    serializer = RentalSerializer(rentals, many=True)
    return JsonResponse(serializer.data, safe=False)

@moderator_required
def approve_rental(request, rental_id):
    rental = Rental.objects.get(id=rental_id)
    rental_title = rental.title
    rental.verified = True
    rental.save()
    return JsonResponse({'message': f'Rental with id {rental_id} and title {rental_title} is now approved'})

    #return redirect('pending_rentals')
