from rest_framework import serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstaUser
        fields = ('nickname_user', 'email_user', 'password', 'image_id')
