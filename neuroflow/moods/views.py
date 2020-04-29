# Django imports
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

# Project imports
from .forms import MoodForm
from .models import Mood
from .helpers import check_if_reset_needed, check_if_longest_streak

# Python imports
from datetime import datetime, timedelta


# Homepage
def home(request):
    return render(request, 'home.html')


# Mood endpoint
@login_required
def mood(request):
    user = request.user
    form = MoodForm(request.POST or None)
    context = {'form': form}

    if request.method == 'POST':
        yesterday = datetime.now() - timedelta(days=1)
        user_moods = Mood.objects.filter(account=user).order_by('-date')

        if user_moods:
            if user_moods[0].date.date() == yesterday.date() or user.streak == 0:
                user.streak += 1
                check_if_longest_streak(user)

        # Second condition with same actions because of constraint error
        elif not user_moods:
            user.streak += 1
            check_if_longest_streak(user)

        mood = Mood.objects.create(emotion=request.POST.get('emotion'))
        mood.account.add(user)
        return redirect('account')

    else:
        return render(request, 'moods.html', context)


# View account
@login_required
def account_view(request):
    context = {}

    if Mood.objects.filter(account=user).count():
        user = request.user
        check_if_reset_needed(user)
        moods = Mood.objects.filter(account=user).order_by("-date")
        context['moods'] = moods
        context['streak'] = user.streak

    return render(request, 'account.html', context)
