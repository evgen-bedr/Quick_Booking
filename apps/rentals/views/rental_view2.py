from django.db.models import Q
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from apps.rentals.models.rental_model import Rental, Image
from apps.rentals.serializers.rental_serializer import RentalSerializer
from apps.rentals.models.tag_model import Tag


class RentalViewSet(viewsets.ModelViewSet):
    queryset = Rental.objects.all()
    serializer_class = RentalSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        tags_data = self.request.data.getlist('tags')
        additional_images_data = self.request.FILES.getlist('additional_images')
        rental = serializer.save(user=self.request.user)
        tags = [Tag.objects.get_or_create(name=tag_name)[0] for tag_name in tags_data]
        rental.tags.set(tags)

        for image in additional_images_data:
            Image.objects.create(rental=rental, image=image)

        rental.save()

    def perform_update(self, serializer):
        instance = self.get_object()
        user = self.request.user

        if user.is_superuser or (hasattr(user, 'role') and user.role == 'Moderator') or user == instance.user:
            tags_data = self.request.data.get('tags', [])
            additional_images_data = self.request.FILES.getlist('additional_images', [])
            rental = serializer.save()

            if tags_data:
                rental.tags.clear()
                for tag_name in tags_data:
                    tag, created = Tag.objects.get_or_create(name=tag_name)
                    rental.tags.add(tag)

            if additional_images_data:
                rental.images.all().delete()
                for image in additional_images_data:
                    Image.objects.create(rental=rental, image=image)

            rental.verified = False
            rental.save()
        else:
            raise PermissionDenied("You do not have permission to edit this rental.")

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user

        if user.is_anonymous:
            return queryset.filter(status=True)

        if user.is_staff or user.is_superuser or (hasattr(user, 'role') and user.role == 'Moderator'):
            return queryset

        return queryset.filter(Q(user=user) | Q(status=True))
