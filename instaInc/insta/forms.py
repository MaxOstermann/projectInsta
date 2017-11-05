from .models import InstaUser, Images, Publications, Comments
from django import forms
from django.contrib.admin import widgets


class OrderForm(forms.ModelForm):
    class Meta:
        model = InstaUser
        fields = ["id", "nickname_user", "email_user", "password", "image_id"]