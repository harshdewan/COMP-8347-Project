from django.db import models


# Create your models here.

class UserLoginCredentials(models.Model):
    userName = models.CharField(max_length=50, blank=False, null=False)
    userPassword = models.CharField(max_length=10, blank=False, null=False)
    userEmail = models.EmailField(blank=False, null=False)

    def __str__(self):
        return self.userName + " " + self.userEmail + " " + self.userPassword


class UserProfileDetails(models.Model):
    userName = models.ForeignKey(UserLoginCredentials, on_delete=models.CASCADE, default=None)
    firstName = models.CharField(max_length=50, blank=False, null=False)
    lastName = models.CharField(max_length=50, blank=False, null=False)
    city = models.CharField(max_length=50, blank=False, null=False)
    country = models.CharField(max_length=50, blank=False, null=False)
    profileImage = models.ImageField(upload_to='images/', default=None)

    def __str__(self):
        return self.firstName + " " + self.lastName + " " + self.userName
