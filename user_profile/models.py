from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class ProfileCategories(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateTimeField(max_length = 100)
    email = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    age = models.PositiveIntegerField(blank=False)
    bio = models.TextField(max_length=500)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """Create or update the user profile."""
    if created:
        UserProfile.objects.create(user=instance)
    else:
        # Get or create the profile to handle existing users
        UserProfile.objects.get_or_create(user=instance)