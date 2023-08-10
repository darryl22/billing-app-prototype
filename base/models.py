from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    userID = models.CharField(max_length=5, unique=True, null=True)
    name = models.CharField(max_length=20, default="")
    usertype = models.CharField(max_length=15, default="consumer")
    nationalID = models.CharField(max_length=15)
    address = models.TextField()
    phone = models.CharField(max_length=20)
    arrears = models.PositiveIntegerField(default=0)
    previousarrears = models.PositiveIntegerField(default=0)
    prepayment = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

class Utility(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.CASCADE, null=True)
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

class Reading(models.Model):
    utility = models.ForeignKey(Utility, on_delete=models.CASCADE)
    reading = models.FloatField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        get_latest_by = 'created'

    def __str__(self):
        n = str(self.reading) + " " + str(self.utility.user.username)
        return n

class Invoice(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    invoiceNo = models.PositiveIntegerField(unique=True, null=True)
    billingmonth = models.CharField(max_length=15)
    year = models.CharField(max_length=5, null=True)
    previousreading = models.FloatField()
    currentreading = models.FloatField()
    consumed = models.FloatField()
    rate = models.CharField(max_length=20)
    consumptionamount = models.FloatField()
    arrears = models.PositiveIntegerField()
    prepayment = models.PositiveIntegerField(default=0)
    amountpayable = models.PositiveIntegerField()
    readingimage = models.ImageField(upload_to='images', null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return str(self.user.username + str(self.id))

class Contract(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    provider = models.ForeignKey(Profile, related_name="provider", on_delete=models.CASCADE)
    consumersignature = models.TextField(null=True)
    suppliersignature = models.TextField(null=True)
    meternumber = models.CharField(max_length=20, null=True)
    rate = models.PositiveIntegerField(null=True)
    deposit = models.FloatField(default=5000)
    refundabledeposit = models.BooleanField(null=True)
    status = models.CharField(max_length=25, default="new")
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)
    
class Receipt(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    paymentmethod = models.CharField(max_length=10)
    amount = models.PositiveIntegerField()
    confirmationcode = models.TextField(max_length=30)
    referencecode = models.CharField(max_length=20)
    currency = models.CharField(max_length=5)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.confirmationcode

