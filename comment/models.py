from django.db import models
from image.models import Images
from insta.models import InstaUser


class Comments(models.Model):
    publication_id = models.ForeignKey(Images, on_delete=models.CASCADE)
    date = models.DateTimeField()
    sender_id = models.ForeignKey(InstaUser, on_delete=models.CASCADE)
    text = models.TextField()


