from .models import InstaUser #, Images, Comments, Likes
from django import forms


class OrderForm(forms.ModelForm):
    class Meta:
        model = InstaUser
        fields = ["id", "nickname_user", "email_user", "password", "image_id"]

