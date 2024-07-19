from django.contrib import admin
from django.utils.html import format_html
from apps.bookings.models.booking_model import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        'booking_link', 'user_link', 'rental_link', 'start_date', 'end_date', 'price', 'status', 'created_at',
        'updated_at'
    )
    list_filter = ('status', 'created_at', 'updated_at', 'start_date', 'end_date')
    search_fields = ('user__username', 'rental__title', 'status')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('user', 'rental', 'start_date', 'end_date', 'price', 'status', 'msg_to_landlord', 'msg_to_user')
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at')
        }),
    )

    def booking_link(self, obj):
        return format_html('<a href="/admin/auth/user/bookings/booking/{}/change/">Booking id - {}</a>', obj.id, obj.id)

    booking_link.short_description = 'Booking'
    booking_link.admin_order_field = 'id'

    def user_link(self, obj):
        return format_html('<a href="/admin/auth/user/users/user/{}/change/">{}</a>', obj.user.id, obj.user.username)

    user_link.short_description = 'User'
    user_link.admin_order_field = 'user'

    def rental_link(self, obj):
        return format_html('<a href="/admin/auth/user/rentals/rental/{}/change/">{}</a>', obj.rental.id,
                           obj.rental.title)

    rental_link.short_description = 'Rental'
    rental_link.admin_order_field = 'rental'

    def has_change_permission(self, request, obj=None):
        if not request.user.is_superuser:
            return False
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        if not request.user.is_superuser:
            return False
        return super().has_delete_permission(request, obj)
