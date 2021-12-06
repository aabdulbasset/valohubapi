from rest_framework import serializers
from . import models
class AccountSerializer():
    class Meta():
        model = models.Accounts
        fields = ('user','riotAuth','entToken','userName')