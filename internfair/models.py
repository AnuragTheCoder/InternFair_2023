from django.db import models
from django.contrib.auth.models import AbstractUser

from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
import os


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.student.user.id, filename)

def user_directory_path1(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.id, filename)

class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_startup = models.BooleanField(default=False)

class StartUps(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    POC = models.CharField(max_length=50)
    email = models.EmailField(max_length=150)
    companyName = models.CharField(max_length=100, default="")
    contact = models.CharField(default="",max_length=10)
    logo = models.ImageField(upload_to='startupLogo',default='./startupLogo/default.png')
    description = models.CharField(max_length=500, default="Edit Profile to add description")
    location = models.CharField(max_length=100, default="Edit profile to add location")


    def __str__(self):
        return self.user.username

class Students(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='student')
    name = models.CharField(max_length=50,default="")
    roll_number = models.CharField(default="",max_length=13)
    department = models.CharField(max_length=50,default="")
    email = models.EmailField(max_length=150,default="")
    contact = models.CharField(default="",max_length=10)
    bio = models.CharField(default="Edit Profile to add bio",max_length=500)
    profilePhoto = models.ImageField(upload_to=user_directory_path,blank=True)
    intern_count = models.IntegerField(default=0)
    def __str__(self):
        return self.user.username


