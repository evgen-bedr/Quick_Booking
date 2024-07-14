# apps/rentals/admin.py
from django.contrib import admin
from django.db import models
from apps.rentals.models.rental_model import Rental
from apps.rentals.models.tag_model import Tag
from apps.rentals.models.image_rental_model import Image
from apps.rentals.widgets.admin_images_widget import AdminImageWidget

class ImageInline(admin.TabularInline):
    model = Image
    extra = 1
    verbose_name = "Additional Image"
    verbose_name_plural = "Additional Images"
    formfield_overrides = {
        models.ImageField: {'widget': AdminImageWidget},
    }

@admin.register(Rental)
class RentalAdmin(admin.ModelAdmin):
    list_display = ('title', 'id', 'user', 'status', 'verified', 'rejection_reason', 'created_at', 'updated_at')
    list_filter = ('status', 'verified', 'created_at', 'updated_at')
    search_fields = ('title', 'description', 'user__username', 'user__email')
    readonly_fields = ('id', 'created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('id', 'title', 'description', 'address', 'city', 'country', 'price', 'rooms', 'property_type', 'status', 'verified', 'rejection_reason', 'user')
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at')
        }),
        ('Other', {
            'fields': ('views_count', 'contact_info', 'tags', 'availability_start_date', 'availability_end_date')
        }),
    )
    filter_horizontal = ('tags',)
    inlines = [ImageInline]

    def save_model(self, request, obj, form, change):
        if not obj.pk:  # если это новый объект
            obj.status = True  # установить status в True
        super().save_model(request, obj, form, change)

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'rental', 'image')

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
