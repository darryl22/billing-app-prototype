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

class Invoice(models.Model):
    user = models.CharField(max_length=30)
    address = models.CharField(max_length=30)
    phone = models.CharField(max_length=20)
    receiver = models.CharField(max_length=30)
    receiverAddress = models.CharField(max_length=30)
    billingmonth = models.CharField(max_length=30)
    previousreading = models.CharField(max_length=20)
    currentreading = models.CharField(max_length=20)
    consumed = models.CharField(max_length=20)
    rate = models.CharField(max_length=20)
    consumptionamount = models.CharField(max_length=20)
    arrears = models.CharField(max_length=20)
    amountpayable = models.CharField(max_length=20)

