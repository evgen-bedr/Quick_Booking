from django.urls import include, path

urlpatterns = [
    path('users/', include('apps.users.urls')),
    path('rentals/', include('apps.rentals.urls')),
    path('search/', include('apps.search_and_filters.urls')),
    path('bookings/', include('apps.bookings.urls')),
    path('reviews/', include('apps.reviews.urls')),
]

# urlpatterns = [
#     path('api/user/', include('apps.users.urls')),
#     path('api/', include('apps.rentals.urls')),
#     path('api/s/', include('apps.search_and_filters.urls')),
#     path('api/b/', include('apps.bookings.urls')),
#     path('api/', include('apps.reviews.urls')),
# ]