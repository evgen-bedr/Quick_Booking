from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from apps.rentals.models.image_rental_model import Image
from apps.rentals.models.rental_model import Rental



class RentalAdminForm(forms.ModelForm):
    additional_images = forms.ModelMultipleChoiceField(
        queryset=Image.objects.none(),
        required=False,
        widget=FilteredSelectMultiple("Additional Images", is_stacked=False)
    )

    class Meta:
        model = Rental
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['additional_images'].queryset = self.instance.additional_images.all()
        else:
            self.fields['additional_images'].queryset = Image.objects.none()
