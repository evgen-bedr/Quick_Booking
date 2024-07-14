# apps/rentals/views/rental_view.py
from django.db import transaction
from django.db.models import Q
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response

from apps.rentals.models.rental_model import Rental
from apps.rentals.models.image_rental_model import Image
from apps.rentals.models.tag_model import Tag

from apps.rentals.serializers.rental_serializer import RentalSerializer

class RentalViewSet(viewsets.ModelViewSet):
    queryset = Rental.objects.all()
    serializer_class = RentalSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'id'

    def perform_create(self, serializer):
        with transaction.atomic():
            tags_data = self.request.data.getlist('tags')
            additional_images_data = self.request.FILES.getlist('additional_images')

            rental = serializer.save(user=self.request.user, status=True)  # Устанавливаем статус в True
            tags = [Tag.objects.get_or_create(name=tag_name)[0] for tag_name in tags_data]
            rental.tags.set(tags)

            for index, image in enumerate(additional_images_data):
                Image.objects.create(rental=rental, image=image, is_main=(index == 0))  # Первое изображение становится основным

            rental.save()

            serializer = self.get_serializer(rental)
            return Response(serializer.data)

    def perform_update(self, serializer):
        instance = self.get_object()
        user = self.request.user
        original_verified = instance.verified  # Сохраняем текущее значение verified

        if user.is_superuser or (hasattr(user, 'role') and user.role == 'Moderator') or user == instance.user:
            tags_data = self.request.data.getlist('tags', None)
            additional_images_data = self.request.FILES.getlist('additional_images', None)
            main_image_id = self.request.data.get('main_image_id', None)

            update_fields = serializer.validated_data.keys()
            changing_sensitive_fields = any(field in update_fields for field in [
                'title',
                'description'
            ]) or bool(additional_images_data)

            rental = serializer.save()

            if changing_sensitive_fields:
                rental.verified = False
            else:
                rental.verified = original_verified

            if tags_data:
                for tag_name in tags_data:
                    tag, created = Tag.objects.get_or_create(name=tag_name.strip())
                    rental.tags.add(tag)

            if additional_images_data:
                for image in additional_images_data:
                    Image.objects.create(rental=rental, image=image)

            if main_image_id:
                rental.images.update(is_main=False)
                main_image = Image.objects.get(id=main_image_id)
                main_image.is_main = True
                main_image.save()

            rental.save()
        else:
            raise PermissionDenied("You do not have permission to edit this rental.")

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        user = self.request.user

        # Проверка прав на удаление
        if not (user.is_superuser or (hasattr(user, 'role') and user.role == 'Moderator') or user == instance.user):
            raise PermissionDenied("You do not have permission to delete this rental.")

        return super().destroy(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset().order_by('-created_at')
        user = self.request.user

        if user.is_anonymous:
            return queryset.filter(status=True, verified=True)

        if user.is_staff or user.is_superuser or (hasattr(user, 'role') and user.role == 'Moderator'):
            return queryset

        return queryset.filter(Q(user=user) | Q(verified=True))

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        ip_address = request.META.get('REMOTE_ADDR')
        instance.increment_views(request.user, ip_address)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def increment_view(self, request, pk=None):
        rental = self.get_object()
        ip_address = request.META.get('REMOTE_ADDR')
        rental.increment_views(request.user, ip_address)
        serializer = self.get_serializer(rental)
        return Response(serializer.data)

    @action(detail=True, methods=['delete'], permission_classes=[IsAuthenticated], parser_classes=[JSONParser])
    def remove_images(self, request, id=None):
        rental = self.get_object()
        user = request.user

        if not (user.is_superuser or (hasattr(user, 'role') and user.role == 'Moderator') or user == rental.user):
            raise PermissionDenied("You do not have permission to delete images for this rental.")

        image_ids = request.data.get('image_ids', [])
        if not image_ids:
            return Response({"detail": "No image IDs provided."}, status=status.HTTP_400_BAD_REQUEST)

        images_to_delete = rental.images.filter(id__in=image_ids)

        if not images_to_delete.exists():
            return Response({"detail": "No images found for the provided IDs."}, status=status.HTTP_404_NOT_FOUND)

        for image in images_to_delete:
            image.delete()

        return Response({"detail": "Images deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
