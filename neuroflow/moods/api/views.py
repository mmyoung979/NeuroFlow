# Django imports
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

# Project imports
from .serializers import MoodSerializer
from ..helpers import calculate_streak_percentile, check_if_longest_streak
from ..models import Mood
from neuroflow.accounts.models import Account

# Python imports
from datetime import datetime, timedelta


# API read info in list
@login_required
@api_view(['GET', 'POST'])
def api_mood_list_view(request):
    user = request.user

    if request.method == 'GET':
        try:
            mood_list = Mood.objects.filter(account=user).order_by('-date')
            context = {'user': user}
            serializer = MoodSerializer(mood_list, many=True, context=context)
            return Response(serializer.data)

        except Mood.DoesNotExist:
            return Response(status.HTTP_404_NOT_FOUND)

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

        mood = Mood()
        mood.save()
        mood.account.add(user)
        serializer = MoodSerializer(mood, data=request.data)
        data = {}

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# API read info for individual moods
@login_required
@api_view(['GET'])
def api_mood_detail_view(request, id):
    try:
        user = request.user
        mood = Mood.objects.get(account=user, id=id)
        user.streak_percentile = calculate_streak_percentile(user)
        user.save()
        serializer = MoodSerializer(mood)
        return Response(serializer.data)

    except Mood.DoesNotExist:
        return Response(status.HTTP_404_NOT_FOUND)
