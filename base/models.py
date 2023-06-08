from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    userID = models.CharField(unique=True, null=True)
    name = models.CharField(max_length=20, default="")
    usertype = models.CharField(max_length=15, default="consumer")
    nationalID = models.CharField(max_length=15)
    address = models.CharField(max_length=30)
    phone = models.CharField(max_length=20)
    arrears = models.CharField(max_length=20, default=0)
    prepayment = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

class Utility(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE, null=True)
    supplier = models.ForeignKey(Profile, related_name="supplier", on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=30)
    unit = models.CharField(max_length=10, null=True)
    rate = models.IntegerField(default=100)
    meternumber = models.CharField(max_length=30, null=True)
    connectiondate = models.CharField(max_length=30, default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username
    
class PaymentDetails(models.Model):
    name = models.OneToOneField(Profile, on_delete=models.CASCADE)
    bankname = models.CharField(max_length=30)
    bankbranch = models.CharField(max_length=30)
    bankaccountno = models.CharField(max_length=30)
    bankaccountname = models.CharField(max_length=30)
    swiftcode = models.CharField(max_length=20)
    paybillno = models.CharField(max_length=15)
    paybillaccountno = models.CharField(max_length=20)

class Reading(models.Model):
    utility = models.ForeignKey(Utility, on_delete=models.CASCADE)
    reading = models.FloatField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        n = str(self.reading) + " " + str(self.utility.user.username)
        return n

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

    def __str__(self):
        return str(self.invoiceNo)

class Contract(models.Model):
    user = models.OneToOneField(Profile, on_delete=models.CASCADE)
    provider = models.OneToOneField(Profile, related_name="provider", on_delete=models.CASCADE)
    consumersignature = models.TextField()
    suppliersignature = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)

