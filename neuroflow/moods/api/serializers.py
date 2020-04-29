# Django imports
from rest_framework import serializers

# Project imports
from ..helpers import calculate_streak_percentile
from ..models import Mood
from neuroflow.accounts.models import Account


# API info for users
class AccountSerializer(serializers.ModelSerializer):
    percentile = serializers.SerializerMethodField('get_percentile')

    class Meta:
        model = Account
        fields = ['streak', 'longest_streak', 'percentile']

    def get_percentile(self, account):
        if account.streak_percentile >= 50:
            return account.streak_percentile

        else:
            return None

# API info for moods
class MoodSerializer(serializers.ModelSerializer):
    account = AccountSerializer(read_only=True, many=True)

    class Meta:
        model = Mood
        fields = ['id', 'emotion', 'date', 'account']
