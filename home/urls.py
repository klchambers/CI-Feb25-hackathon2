from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home/templates/home/team.html', views.team, name='team'),
    path('home/templates/home/cookies.html', views.cookies, name='cookies'),
    path('home/templates/home/service.html', views.service, name='service'),
    path('home/templates/home/privacy.html', views.privacy, name='privacy'),
    path('home/templates/home/safety.html', views.safety, name='safety'),
]
