# Django imports
from django.db import models

# Project imports
from ..accounts.models import Account


class Mood(models.Model):
    emotion = models.CharField(max_length=20)
    date = models.DateTimeField(auto_now=True, verbose_name="Date Entered")
    account = models.ManyToManyField(Account)
