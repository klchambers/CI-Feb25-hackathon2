from django.urls import path
from . import views

urlpatterns = [
    path('', views.matches, name='match-making'),
]