from django.db import models

# Create your models here.
class ProfileCategories(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateTimeField(max_length = 100)
    email = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    age = models.PositiveIntegerField(max_length=3)
    bio = models.TextField(max_length=500)
