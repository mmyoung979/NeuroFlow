# Django imports
from django.urls import path

# Project imports
from . import views

app_name = 'mood'

urlpatterns = [
    path('', views.api_mood_list_view),
    path('<int:id>/', views.api_mood_detail_view),
]
