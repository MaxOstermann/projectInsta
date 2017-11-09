from .models import InstaUser, Images, Comments
from django import forms
from django.contrib.admin import widgets


class OrderForm(forms.ModelForm):
    class Meta:
        model = InstaUser
        fields = ["id", "nickname_user", "email_user", "password", "image_id"]


class PhotoForm(forms.ModelForm):
    class Meta:
        model = Images
        fields = ["id", "description", "image_id", "created_by"]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ["publication_id", "date", "sender_id", "text"]