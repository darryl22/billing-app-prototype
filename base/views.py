from django.shortcuts import render, redirect
from .models import Utility, Reading, Profile, Contract, Invoice, Receipt
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.conf import settings
import plotly.express as px
import datetime
import subprocess
from django.core.mail import send_mail
from django.conf import settings
from twilio.rest import Client
import requests
import json
import random

# Create your views here.

def home(request):
    return render(request, 'home.html')

def loginUser(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            finduser = User.objects.get(username = username)
            if finduser is not None:
                user = authenticate(request, username = username, password = password)
                if user is not None:
                    login(request, user)
                    return redirect("dashboard")
            else:
                messages.error(request, "invalid login credentials")
        except:
            messages.error(request, "user not found")

    return render(request, 'login.html')

def signup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirmpassword = request.POST.get("confirm-password")
        phone = request.POST.get("phone")
        address = request.POST.get("address")
        nationalID = request.POST.get("nationalID")
        firstname = request.POST.get("firstname")
        lastname = request.POST.get("lastname")

        if password == confirmpassword:
            user = User.objects.create_user(username, email, password)
            user.first_name = firstname
            user.last_name = lastname
            user.save()
            profile = Profile(user = user, name = user.username, usertype = "consumer", nationalID = nationalID, address = address, phone = phone)
            profile.save()
            utility = Utility(user = user, name = "Water", unit = "Liters")
            utility.save()
            reading = Reading(utility = utility, reading = 0)
            reading.save()
            login(request, user)

            twilio_sid = settings.TWILIO_ACCOUNT_SID
            twilio_auth_token = settings.TWILIO_AUTH_TOKEN

            client = Client(twilio_sid, twilio_auth_token)

            message = client.messages.create(
                body='Welcome to the Kobby Billing App, you will be receiving updated on billings and other information from this line',
                from_='whatsapp:+14155238886',
                to='whatsapp:+254708323035'
            )

            message = client.messages.create(
                body='Welcome to the Kobby Billing App, you will be receiving updated on billings and other information from this line',
                from_='+18148015643',
                to='+254708323035'
            )
            return redirect("dashboard")
                
        else:
            messages.error(request, "passwords did not match")
    return render(request, 'signup.html')

def logoutUser(request):
    logout(request)
    return redirect('main')

@login_required(login_url="login")
def dashboard(request):
    ctx = []
    labels = []
    data = []
    line = 0
    image = []

    if request.user.profile.usertype == "supplier":
        utility = Utility.objects.all()
        for x in utility:
            ctx.append(x)
    else:
        utility = Utility.objects.get(user = request.user)
        readings = Reading.objects.filter(utility = utility)
        try:
            readingimage = Invoice.objects.filter(user = request.user).latest("created")
            image.append(readingimage)
        except:
            print("no invoice")
        unit = utility.unit
        for x in readings:
            data.append(x.reading)
            labels.append(x.created)
        ctx.append(utility)

        fig = px.line(
            x = labels,
            y = data,
            title = "meter readings",
            markers = True,
            labels = {
                "x": "dates",
                "y": unit,
                "variable": "utilities"
            },
            template = "simple_white",
            # height = 580,
            # width = 1000
        )
        line = fig.to_html()

    if request.method == "POST":

        latestinvoice = Invoice.objects.latest("created")
        day = datetime.datetime.now()
        image = request.FILES["readingimage"]
        reading = float(request.POST.get("reading"))
        utilId = request.POST.get("utility")
        billingmonth = request.POST.get("billingmonth")
        util = Utility.objects.get(id = utilId)
        latest_reading = Reading.objects.filter(utility = util).latest("created")
        profile = Profile.objects.get(user = util.user)
        amount = round(((reading - latest_reading.reading) * util.rate), 2)

        if profile.prepayment >= amount:
            newprepayment = profile.prepayment - amount
            print(newprepayment)
            profile.prepayment = newprepayment
            profile.save()

            invoice = Invoice(
                user = util.user,
                invoiceNo = latestinvoice.invoiceNo + 1,
                billingmonth = billingmonth,
                year = day.strftime("%Y"), 
                previousreading = latest_reading.reading,
                currentreading = reading,
                consumed = round((reading - latest_reading.reading), 2),
                rate = util.rate,
                consumptionamount = amount,
                arrears = profile.arrears,
                prepayment = profile.prepayment,
                amountpayable = profile.arrears,
                readingimage = image
                )
            invoice.save()
        else:
            prevarrears = profile.arrears
            newarrears = profile.arrears + amount - profile.prepayment
            profile.previousarrears = prevarrears
            profile.arrears = newarrears
            profile.prepayment = 0
            profile.save()

            invoice = Invoice(
                user = util.user,
                invoiceNo = latestinvoice.invoiceNo + 1,
                billingmonth = billingmonth,
                year = day.strftime("%Y"),
                previousreading = latest_reading.reading,
                currentreading = reading,
                consumed = round((reading - latest_reading.reading), 2),
                rate = util.rate,
                consumptionamount = amount,
                arrears = prevarrears,
                prepayment = profile.prepayment,
                amountpayable = newarrears,
                readingimage = image
                )
            invoice.save()

        r = Reading(utility = util, reading = reading)
        r.save()
        subject = "Billing information"
        message = f"Hello {profile.name}, your water supply has been billed for this month.\n\n Current reading : {reading} \n difference : {reading - latest_reading.reading} \n arrears : {profile.arrears}."
        sender = settings.EMAIL_HOST_USER
        receiver = ['darrylandrew22@gmail.com']
        send_mail(subject, message, sender, receiver)
    
    return render(request, 'dashboard.html', {"data": ctx, "length": len(ctx), "line": line, "image": image, "imagelen": len(image)})

def UtilityDetails(request, pk):
    
    invoices = Invoice.objects.filter(user = request.user)
    return render(request, 'utilityDetails.html', {"invoices" : invoices})

def invoice(request):
    try:
        invoice = Invoice.objects.filter(user = request.user).latest("created")
    except:
        return redirect("dashboard")

    ctx = {
        "invoice": invoice,
        "previousreading": "{:,}".format(invoice.previousreading),
        "currentreading": "{:,}".format(invoice.currentreading),
        "consumed": "{:,}".format(round(invoice.consumed, 2)),
        "consumptionamount": "{:,}".format(invoice.consumptionamount),
        "arrears": "{:,}".format(invoice.arrears),
        "prepayment": "{:,}".format(invoice.prepayment),
        "amountpayable": "{:,}".format(invoice.amountpayable),
    }
    return render(request, 'invoice.html', ctx)

def contract(request, pk):

    profile = Profile.objects.get(name = pk)
    consumer = User.objects.get(username = pk)
    supplier = Profile.objects.get(name = "supplier")
    utility = Utility.objects.get(user = profile.user)
    print(utility)
    day = datetime.datetime.now()

    try:
        contract = Contract.objects.get(user = consumer)
    except:
        contract = Contract(user = consumer, provider = supplier)
        contract.save()

    ctx = {
        "profile": profile,
        "contract": contract,
        "day": day.strftime("%d"),
        "month": day.strftime("%B"),
        "year": day.strftime("%Y"),
        "utility": utility
    }

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "supplier":

            supplierSignature = request.POST.get("suppliersignInput")
            rate = request.POST.get("rate")
            meternumber = request.POST.get("meternumber")
            print("supplier signature")
            print("rate", rate)
            print("neter number", meternumber)
            if len(supplierSignature) > 2:
                contract.status = "signed by supplier"
                contract.suppliersignature = supplierSignature
                contract.meternumber = meternumber
                contract.rate = rate
                contract.save()
                utility.rate = rate
                utility.meternumber = meternumber
                utility.save()
                print("signed by supplier")

        elif action == "consumer":

            consumerSignature = request.POST.get("consumersignInput")
            print("consumer signature")
            if len(consumerSignature) > 2:
                contract.status = "complete"
                contract.consumersignature = consumerSignature
                contract.save()
                print("signed by consumer")

    return render(request, 'contract.html', ctx)

def ProfilePage(request):

    profile = Profile.objects.get(name = request.user.username)
    user = User.objects.get(username = request.user.username)

    if (request.method == "POST"):
        action = request.POST.get("action")
        if action == "1":
            username = request.POST.get("username")
            firstname = request.POST.get("firstname")
            lastname = request.POST.get("lastname")
            email = request.POST.get("email")
            phone = request.POST.get("phone")
            address = request.POST.get("address")

            user.username = username
            user.first_name = firstname
            user.last_name = lastname
            user.email = email
            profile.phone = phone
            profile.address = address
            user.save()
            profile.save()
            return redirect("profile")
        elif action == "2":
            currentpassword = request.POST.get("currentpassword")
            newpassword = request.POST.get("newpassword")
            confirmpassword = request.POST.get("confirmpassword")
            if user.check_password(currentpassword):
                if newpassword == confirmpassword:
                    user.set_password(newpassword)
                    user.save()
                else:
                    messages.error(request, "new passwords did not match")
            else:
                messages.error(request, "you entered the wrong current password")
            

    return render(request, 'profile.html', {"user": request.user})

def backupPage(request):
    prs = subprocess.run('python manage.py dumpdata --indent 4 > newdata.json', shell=True)
    print("status :", prs.returncode)
    return render(request, 'backup.html')

def payment(request):

    amount = int(request.GET.get("amount"))
    redirecturl = ""
    authData = json.dumps({"consumer_key" : settings.PESAPAL_CONSUMER_KEY, "consumer_secret" : settings.PESAPAL_CONSUMER_SECRET})
    auth_request = requests.post("https://cybqa.pesapal.com/pesapalv3/api/Auth/RequestToken", headers = {"Content-Type" : "application/json", "Accepts" : "application/json"}, data = authData)

    if auth_request.status_code == 200:
        auth_token = auth_request.json()['token']

        ipnHeader = {"Authorization" : f"Bearer {auth_token}", "Content-Type" : "application/json", "Accepts" : "application/json"}
        ipnData = json.dumps({
            "url" : f"https://d68c-41-215-18-254.ngrok-free.app/paymentIPN/{request.user.username}", 
            "ipn_notification_type" : "GET"
        })
        ipn_request = requests.post("https://cybqa.pesapal.com/pesapalv3/api/URLSetup/RegisterIPN", headers = ipnHeader, data = ipnData)
        if ipn_request.status_code == 200:
            ipn_id = ipn_request.json()['ipn_id']
            print("ipnid", ipn_id)

            payment_body = json.dumps({
                "id": "WATERPAYMENT-" + str(random.randint(100000, 999999)),
                "currency": "KES",
                "amount": amount,
                "description": "Arrears payment",
                "callback_url": "https://d68c-41-215-18-254.ngrok-free.app/paymentCallback",
                "notification_id": ipn_id,
                "billing_address": {
                    "email_address": "darrylandrew22@gmail.com",
                    "phone_number": "0708323035",
                    "country_code": "KE",
                    "first_name": request.user.first_name,
                    "middle_name": "",
                    "last_name": request.user.last_name,
                    "line_1": "",
                    "line_2": "",
                    "city": "",
                    "state": "",
                    "postal_code": None,
                    "zip_code": None
                }
            })

            payment_request = requests.post("https://cybqa.pesapal.com/pesapalv3/api/Transactions/SubmitOrderRequest", headers = {"Authorization" : f"Bearer {auth_token}", "Content-Type" : "application/json"}, data = payment_body)
            print("payment", payment_request.json())
            redirecturl = payment_request.json()['redirect_url']
    return render(request, 'payment.html', {"redirecturl" : redirecturl})

def paymentIPN(request, pk):
    profile = Profile.objects.get(name = pk)
    OrderTrackingId = request.GET.get("OrderTrackingId")
    OrderMerchantReference = request.GET.get("OrderMerchantReference")
    OrderNotificationType = request.GET.get("OrderNotificationType")

    authData = json.dumps({"consumer_key" : settings.PESAPAL_CONSUMER_KEY, "consumer_secret" : settings.PESAPAL_CONSUMER_SECRET})
    auth_request = requests.post("https://cybqa.pesapal.com/pesapalv3/api/Auth/RequestToken", headers = {"Content-Type" : "application/json", "Accepts" : "application/json"}, data = authData)
    
    if auth_request.status_code == 200:
        
        auth_token = auth_request.json()['token']
        statusHeader = {"authorization" : f"Bearer {auth_token}", "Content-Type" : "application/json", "Accepts" : "application/json"}
        payment_status = requests.get(f"https://cybqa.pesapal.com/pesapalv3/api/Transactions/GetTransactionStatus?orderTrackingId={OrderTrackingId}", headers = statusHeader)
        if payment_status.status_code == 200:
            print(payment_status.json())

            if payment_status.json()['status'] == '200' and payment_status.json()['status_code'] == 1:
                print("payment successful")
                if payment_status.json()['amount'] > profile.arrears:
                    profile.prepayment = (payment_status.json()['amount'] - profile.arrears) + profile.prepayment
                    profile.arrears = 0
                    profile.save()
                else:
                    profile.arrears = profile.arrears - payment_status.json()['amount']
                    profile.save()
                
                receipt = Receipt(
                    user = profile.user, 
                    paymentmethod = payment_status.json()['payment_method'],
                    amount = payment_status.json()['amount'],
                    confirmationcode = payment_status.json()['confirmation_code'],
                    referencecode = payment_status.json()['merchant_reference'],
                    currency = payment_status.json()['currency']
                )
                receipt.save()

            return JsonResponse({
                "orderNotificationType" : OrderNotificationType,
                "orderTrackingId" : OrderTrackingId,
                "orderMerchantReference" : OrderMerchantReference,
                "status" : 200
            })
        else:
            print(payment_status.json()['description'])
            return JsonResponse({
                "orderNotificationType" : OrderNotificationType,
                "orderTrackingId" : OrderTrackingId,
                "orderMerchantReference" : OrderMerchantReference,
                "status" : 500
            })
    else:
        print("error getting token")
        return JsonResponse({
            "orderNotificationType" : OrderNotificationType,
            "orderTrackingId" : OrderTrackingId,
            "orderMerchantReference" : OrderMerchantReference,
            "status" : 500
        })

def paymentCallback(request):

    return render(request, 'paymentCallback.html')