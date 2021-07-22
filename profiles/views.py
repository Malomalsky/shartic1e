from django.shortcuts import render, redirect, reverse
from .models import Profile
from .forms import RegisterForm

def leaderboard(request):
    profiles = Profile.objects.all()[:10]
    return render(request, 'profiles/leaderboard.html', {'profiles': profiles})


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('index'))
        else:
            return render(request, 'profiles/register.html', {'form': form })
    else:
        form = RegisterForm()
        context = {
            'form': form
        }
        return render(request, 'profiles/register.html', context=context)

