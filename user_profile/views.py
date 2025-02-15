from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def profile_view(request):
    return render(request, 'user_profile/user_profile.html')