# Project imports
from .models import Mood
from neuroflow.accounts.models import Account

# Python imports
from datetime import datetime, timedelta


# Check if user didn't record mood yesterday
def check_if_reset_needed(user):
    yesterday = datetime.now() - timedelta(days=1)
    if Mood.objects.all().count() > 0:
        if Mood.objects.last().date.date() < yesterday.date():
            user.streak = 0
            user.save()


# Streak percentile = rank (descending) / # of active accounts
def calculate_streak_percentile(user):
    active_accounts = Account.objects.filter(longest_streak__gte=1).count()
    index = Account.objects.filter(longest_streak__range=[1, user.streak]).count()

    if index > 0 and active_accounts:
        return int(index / active_accounts * 100)

    else:
        return user.streak_percentile


def check_if_longest_streak(user):
    if user.streak > user.longest_streak:
        user.longest_streak = user.streak

    user.streak_percentile = calculate_streak_percentile(user)
    user.save()
