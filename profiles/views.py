from django.shortcuts import render
from .models import Profile


def leaderboard(request):
    profiles = Profile.objects.all()[:10]
    return render(request, 'profiles/leaderboard.html', {'profiles': profiles})
