from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Event(models.Model):
    name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    image = models.ImageField(upload_to='event_images/', null=True, blank=True)  # New field for event image
    location = models.CharField(max_length=255, default='Windsor, ON')

    def __str__(self):
        return self.name
