from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from apps.rentals.models.rental_model import Rental
from apps.rentals.serializers.rental_serializer import RentalSerializer
from apps.core.permissions.moderator_or_super import IsModeratorOrSuperUser


class RentalAdminViewSet(viewsets.ModelViewSet):
    queryset = Rental.objects.all()
    serializer_class = RentalSerializer
    permission_classes = [IsModeratorOrSuperUser]

    def get_queryset(self):
        return Rental.objects.all()

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        rental = self.get_object()
        rental.verified = True
        rental.save()
        return Response({'status': 'approved'})
