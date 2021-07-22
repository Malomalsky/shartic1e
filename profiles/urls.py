from django.urls import path, include
from .views import leaderboard, register

app_name = 'profiles'

urlpatterns = [
    path('leaderboard/', leaderboard, name='leaderboard'),
    path('register/', register, name='register'),
    path('accounts/', include("django.contrib.auth.urls")),
]
