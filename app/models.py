from django.db import models
from django.contrib.auth.models import AbstractUser



class UserProfile(AbstractUser):
    age = models.IntegerField(verbose_name="年龄",default="1")




