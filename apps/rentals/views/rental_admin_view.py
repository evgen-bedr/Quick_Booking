from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from apps.rentals.models.rental_model import Rental
from apps.rentals.serializers.rental_serializer import RentalSerializer
from apps.core.permissions.moderator_or_super import IsModeratorOrSuperUser


class RentalAdminViewSet(viewsets.ModelViewSet):
    """
    Handles administrative operations for rental properties.

    @queryset: Rental.objects.all() : QuerySet : All rentals
    @serializer_class: RentalSerializer : Serializer : Rental serializer
    @permission_classes: [IsModeratorOrSuperUser] : List : Permissions required to access the view
    """
    queryset = Rental.objects.all()
    serializer_class = RentalSerializer
    permission_classes = [IsModeratorOrSuperUser]

    def get_queryset(self):
        """
        Retrieve the queryset of all rental properties.

        @param self: RentalAdminViewSet : Instance of the viewset

        @return: QuerySet : All rentals
        """
        return Rental.objects.all()

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        """
        Approve a rental listing by setting its verified status to True.

        @param request: Request : Request object containing the request data
        @param pk: str : Primary key of the rental property

        @return: Response : JSON response with approval status
        """
        rental = self.get_object()
        rental.verified = True
        rental.save()
        return Response({'status': 'approved'})
