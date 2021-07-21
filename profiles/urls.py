from django.urls import path
from .views import leaderboard

app_name = 'profiles'

urlpatterns = [
    path('leaderboard/', leaderboard, name='leaderboard')
]
