from django.forms.widgets import ClearableFileInput


class AdminImageWidget(ClearableFileInput):
    template_name = 'admin_images_widget.html'

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        if value and getattr(value, 'url', None):
            context['widget']['image_url'] = value.url
        return context
