from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from user_profile.models import UserProfile

class Command(BaseCommand):
    help = 'Creates missing user profiles for existing users'

    def handle(self, *args, **kwargs):
        User = get_user_model()
        for user in User.objects.all():
            UserProfile.objects.get_or_create(user=user)