from django.db import models
from image_cropping import ImageCroppingMixin


class InstaUser(ImageCroppingMixin, models.Model):
    id = models.AutoField(primary_key=True)
    nickname_user = models.CharField(max_length=100, unique=True)
    email_user = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    image_id = models.ImageField(blank=True, upload_to="insta/photos")

    def __str__(self):
        return self.nickname_user


class Follows(models.Model):
        man = models.ForeignKey(InstaUser, on_delete=models.CASCADE, related_name='user_im')
        created = models.DateTimeField(auto_now_add=True)
        follow_to = models.ForeignKey(InstaUser, on_delete=models.CASCADE, related_name='user_out')
