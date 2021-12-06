from django.db import models
from django.contrib.auth.models import User
class Accounts(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    email = models.CharField(max_length=200,unique=True)
    hashedPass = models.CharField(max_length=200)
    userName = models.CharField(max_length=150,default="None")
    def __str__(self):
        return self.userName
# Create your models here.
