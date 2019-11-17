from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class UserProfileInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='basic_app/profile_pics',blank=True)

    def __str__(self):
        return self.user.username


class Video(models.Model):
    name= models.CharField(max_length=500)
    videofile= models.FileField(upload_to='videos/', null=True, verbose_name="")
    description =models.CharField(max_length=500,default=1)
    tags =models.CharField(max_length=225,default=1)
    categories =models.CharField(max_length=225,default=1)

    def get_absolute_url(self):
        return reverse ("video_app:detail",kwargs={'pk':self.pk})


    def __str__(self):
       return str(self.videofile)
