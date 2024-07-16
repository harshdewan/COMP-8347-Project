from django.db import models
from django.contrib.auth.models import User
from MainPage.models import *


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    city = models.CharField(max_length=50, blank=False, null=False)
    country = models.CharField(max_length=50, blank=False, null=False)
    profileImage = models.ImageField(upload_to='images/', default=None)
    eventInterested = models.ForeignKey(EventCategory, on_delete=models.CASCADE, default=1)


