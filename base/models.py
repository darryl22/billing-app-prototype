from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Utility(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE, null=True)
    name = models.CharField(max_length=30)
    unit = models.CharField(max_length=10, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Reading(models.Model):
    utility = models.ForeignKey(Utility, on_delete=models.CASCADE)
    reading = models.PositiveIntegerField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.reading)
