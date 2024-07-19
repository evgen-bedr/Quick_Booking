from django.contrib import admin
from django.utils.html import format_html
from apps.reviews.models.review_model import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user_link', 'rental_link', 'booking_link', 'rating', 'comment', 'status', 'created_at', 'updated_at'
    )
    list_filter = ('rating', 'status', 'created_at', 'updated_at')
    search_fields = ('user__username', 'rental__title', 'comment')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('user', 'rental', 'booking', 'rating', 'comment', 'status')
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at')
        }),
    )

    def user_link(self, obj):
        return format_html('<a href="/admin/auth/user/users/user/{}/change/">{}</a>', obj.user.id, obj.user.username)

    user_link.short_description = 'User'
    user_link.admin_order_field = 'user'

    def rental_link(self, obj):
        return format_html('<a href="/admin/auth/user/rentals/rental/{}/change/">{}</a>', obj.rental.id,
                           obj.rental.title)

    rental_link.short_description = 'Rental'
    rental_link.admin_order_field = 'rental'

    def booking_link(self, obj):
        return format_html('<a href="/admin/auth/user/bookings/booking/{}/change/">{}</a>', obj.booking.id,
                           obj.booking.id)

    booking_link.short_description = 'Booking'
    booking_link.admin_order_field = 'booking'

    def has_change_permission(self, request, obj=None):
        if not request.user.is_superuser:
            return False
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        if not request.user.is_superuser:
            return False
        return super().has_delete_permission(request, obj)
