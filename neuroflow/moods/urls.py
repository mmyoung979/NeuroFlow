# Django imports
from django.contrib import admin
from django.urls import path

# Project imports
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('moods/', views.mood, name='mood'),
    path('account/', views.account_view, name='account'),
]
