# accounts/models.py
from django.db import models

class UserData(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)  # unique validation
    password = models.CharField(max_length=128)
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.name
