from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=20, default="")
    usertype = models.CharField(max_length=15, default="consumer")
    nationalID = models.CharField(max_length=15)
    address = models.CharField(max_length=30)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Utility(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE, null=True)
    supplier = models.OneToOneField(Profile, related_name="supplier", on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=30)
    unit = models.CharField(max_length=10, null=True)
    rate = models.IntegerField(default=100)
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
    approved = models.BooleanField(default=False)

