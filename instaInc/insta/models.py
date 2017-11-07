from django.db import models


class InstaUser(models.Model):
    id = models.AutoField(primary_key=True)
    nickname_user = models.CharField(max_length=100, unique=True)
    email_user = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    image_id = models.ImageField(blank=True, upload_to="insta/photos")

    def __str__(self):
        return self.nickname_user


class Images(models.Model):
    id = models.AutoField(primary_key=True)
    url = models.CharField(max_length=100)
    created_by = models.ForeignKey(InstaUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField()


class Publications(models.Model):
    description = models.CharField(max_length=200)
    sender_id = models.ForeignKey(InstaUser, on_delete=models.CASCADE)
    publicated_at = models.DateTimeField()
    content_id = models.ForeignKey(Images, on_delete=models.CASCADE)


class Comments(models.Model):
    publication_id = models.ForeignKey(Publications, on_delete=models.CASCADE)
    date = models.DateTimeField()
    sender_id = models.ForeignKey(InstaUser, on_delete=models.CASCADE)
# Create your models here.