from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from apps.rentals.models.rental_model import Rental
from apps.rentals.serializers.rental_serializer import RentalSerializer
from django.shortcuts import render, redirect
from apps.core.permissions.moderator_or_super import IsModeratorOrSuperUser

class PendingRentalViewSet(viewsets.ModelViewSet):
    queryset = Rental.objects.filter(verified=False, rejected=False).order_by('-created_at')
    serializer_class = RentalSerializer
    permission_classes = [IsModeratorOrSuperUser]

@api_view(['GET'])
@permission_classes([IsModeratorOrSuperUser])
def pending_rentals_view(request):
    rentals = Rental.objects.filter(verified=False, rejected=False).order_by('-created_at')
    return render(request, 'pending_rentals.html', {'rentals': rentals})

@api_view(['GET'])
@permission_classes([IsModeratorOrSuperUser])
def pending_rentals_data(request):
    rentals = Rental.objects.filter(verified=False, rejected=False).order_by('-created_at').values('id', 'title', 'description')
    return JsonResponse(list(rentals), safe=False)

@api_view(['GET'])
@permission_classes([IsModeratorOrSuperUser])
def pending_rentals_list(request):
    rentals = Rental.objects.filter(verified=False, rejected=False).order_by('-created_at')
    serializer = RentalSerializer(rentals, many=True)
    return JsonResponse(serializer.data, safe=False)

@api_view(['GET', 'POST'])
@permission_classes([IsModeratorOrSuperUser])
def approve_rental(request, rental_id):
    rental = Rental.objects.get(id=rental_id)
    rental.verified = True
    rental.save()
    return redirect('pending_rentals')

@api_view(['GET', 'POST'])
@permission_classes([IsModeratorOrSuperUser])
def reject_rental(request, rental_id):
    rental = Rental.objects.get(id=rental_id)
    rejection_reason = request.POST.get('rejection_reason', '')
    rental.rejection_reason = rejection_reason
    rental.rejected = True
    rental.save()
    return redirect('pending_rentals')
