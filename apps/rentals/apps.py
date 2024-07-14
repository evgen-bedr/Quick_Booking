from django.apps import AppConfig


class RentalsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.rentals'

    def ready(self):
        import apps.rentals.signals.delete_image_file_signal
        import apps.rentals.signals