from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from apps.rentals.models.rental_model import Rental
from apps.rentals.serializers.rental_serializer import RentalSerializer
from django.shortcuts import render, redirect
from apps.core.permissions.moderator_or_super import IsModeratorOrSuperUser


class PendingRentalViewSet(viewsets.ModelViewSet):
    """
    Handles operations for listing pending rentals.

    @queryset: Rental.objects.filter(verified=False, rejected=False).order_by('-updated_at') : QuerySet : Pending rentals ordered by updated date
    @serializer_class: RentalSerializer : Serializer : Rental serializer
    @permission_classes: [IsModeratorOrSuperUser] : List : Permissions required to access the view
    """
    queryset = Rental.objects.filter(verified=False, rejected=False).order_by('-updated_at')
    serializer_class = RentalSerializer
    permission_classes = [IsModeratorOrSuperUser]


@api_view(['GET'])
@permission_classes([IsModeratorOrSuperUser])
def pending_rentals_view(request):
    """
    Render a template with the list of pending rentals.

    @param request: Request : Request object containing the request data

    @return: Response : Rendered HTML template with pending rentals
    """
    rentals = Rental.objects.filter(verified=False, rejected=False).order_by('-created_at')
    return render(request, 'pending_rentals.html', {'rentals': rentals})


@api_view(['GET'])
@permission_classes([IsModeratorOrSuperUser])
def pending_rentals_data(request):
    """
    Retrieve the data of pending rentals in JSON format.

    @param request: Request : Request object containing the request data

    @return: JsonResponse : JSON response with the list of pending rentals
    """
    rentals = Rental.objects.filter(verified=False, rejected=False).order_by('-created_at').values('id', 'title',
                                                                                                   'description')
    return JsonResponse(list(rentals), safe=False)


@api_view(['GET'])
@permission_classes([IsModeratorOrSuperUser])
def pending_rentals_list(request):
    """
   Retrieve the list of pending rentals with detailed information in JSON format.

   @param request: Request : Request object containing the request data

   @return: JsonResponse : JSON response with detailed information of pending rentals
   """
    rentals = Rental.objects.filter(verified=False, rejected=False).order_by('-created_at')
    serializer = RentalSerializer(rentals, many=True)
    return JsonResponse(serializer.data, safe=False)


@api_view(['GET', 'POST'])
@permission_classes([IsModeratorOrSuperUser])
def approve_rental(request, rental_id):
    """
    Approve a pending rental by setting its verified status to True.

    @param request: Request : Request object containing the request data
    @param rental_id: int : ID of the rental to be approved

    @return: Response : Redirect to the pending rentals page
    """
    rental = Rental.objects.get(id=rental_id)
    rental.verified = True
    rental.save()
    return redirect('pending_rentals')


@api_view(['GET', 'POST'])
@permission_classes([IsModeratorOrSuperUser])
def reject_rental(request, rental_id):
    """
    Reject a pending rental by setting its rejected status to True and adding a rejection reason.

    @param request: Request : Request object containing the request data
    @param rental_id: int : ID of the rental to be rejected

    @return: Response : Redirect to the pending rentals page
    """
    rental = Rental.objects.get(id=rental_id)
    rejection_reason = request.POST.get('rejection_reason', '')
    rental.rejection_reason = rejection_reason
    rental.rejected = True
    rental.save()
    return redirect('pending_rentals')
