from rest_framework import serializers
from .models import *


class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = ('publication_id', 'date', 'sender_id', 'text')


class CommentsSerializer2(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = ('publication_id', 'text')