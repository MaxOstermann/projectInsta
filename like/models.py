from django.db import models
from image.models import Images
from insta.models import InstaUser


class Likes(models.Model):
    picture = models.ForeignKey(Images, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    sender_id = models.ForeignKey(InstaUser, on_delete=models.CASCADE)

