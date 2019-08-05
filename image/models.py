from django.db import models
from image_cropping import ImageCroppingMixin
from insta.models import InstaUser

class Images(ImageCroppingMixin, models.Model):
    id = models.AutoField(primary_key=True)
    created_by = models.ForeignKey(InstaUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True, blank=True)
    description = models.CharField(max_length=200)
    image_id = models.ImageField(upload_to="insta/photos")

# Create your models here.
