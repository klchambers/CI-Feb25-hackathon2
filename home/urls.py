from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home/templates/home/team.html', views.team, name='team'),
]
