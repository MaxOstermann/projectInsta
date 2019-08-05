from .models import Images
from django import forms


class PhotoForm(forms.ModelForm):
    class Meta:
        model = Images
        fields = ["id", "description", "image_id", "created_by"]
