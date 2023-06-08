from django.shortcuts import render, redirect
from .models import Utility, Reading, Profile, Contract
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
import plotly.express as px
from django.http import HttpResponse
import datetime
import re
import subprocess
import requests
from django.conf import settings
import base64
from django.views.decorators.csrf import csrf_exempt
import hashlib

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
        usertype = request.POST.get("usertype")
        firstname = request.POST.get("firstname")
        lastname = request.POST.get("lastname")

        if password == confirmpassword:
            user = User.objects.create_user(username, email, password)
            user.first_name = firstname
            user.last_name = lastname
            user.save()
            profile = Profile(user = user, name = user.username, usertype = usertype, nationalID = nationalID, address = address, phone = phone)
            profile.save()
            login(request, user)
            if usertype == "supplier":
                return redirect("paymentDetails")
            else:
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
    if request.user.is_authenticated:
        if request.user.profile.usertype == "supplier":
            utility = Utility.objects.all()
            for x in utility:
                ctx.append(x)
        else:
            utility = Utility.objects.get(user = request.user)
            readings = Reading.objects.filter(utility = utility)
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
        reading = request.POST.get("reading")
        utilId = request.POST.get("utility")
        util = Utility.objects.get(id = utilId)
        print(util.user)
        r = Reading(utility = util, reading = reading)
        r.save()
    
    return render(request, 'dashboard.html', {"data": ctx, "length": len(ctx), "line": line})

def UtilityDetails(request, pk):
    data = []
    labels = []
    dif = []
    amount = []
    utility = Utility.objects.get(user = request.user)
    readings = Reading.objects.filter(utility = utility)
    temp = 0
    for x in readings:
        data.append(x.reading)
        labels.append(x.created)
        dif.append(int(x.reading) - temp)
        amount.append((int(x.reading) - temp) * utility.rate)
        temp = int(x.reading)
    
    unit = utility.unit
    if len(data) < 2:
        return redirect("dashboard")

    x = list(zip(data, dif, labels, amount))

    ctx = {
        "utility": utility,
        "unit": unit,
        "data": x
    }
    return render(request, 'utilityDetails.html', ctx)

def invoice(request):
    data = []
    labels = []
    profile = Profile.objects.get(name = request.user)
    arrears = int(profile.arrears)
    prepayment = profile.prepayment
    utility = Utility.objects.get(user = request.user)
    readings = Reading.objects.filter(utility = utility)
    for x in readings:
        data.append(x.reading)
        labels.append(x.created)
    consumed = data[-1] - data[-2]
    consumedAmount = round((consumed * utility.rate), 2)
    day = datetime.datetime.now()
    amountpayable = consumedAmount + arrears - prepayment

    ctx = {
        "utility": utility,
        "current": data[-1],
        "previous": data[-2],
        "consumed": round(consumed, 2),
        "consumedAmount": "{:,}".format(consumedAmount),
        "amountpayable": "{:,}".format(amountpayable),
        "month": day.strftime("%B"),
        "day": day.strftime("%d"),
        "year": day.strftime("%Y"),
        "profile": profile,
        "arrears": "{:,}".format(arrears),
        "prepayment": "{:,}".format(prepayment)
    }
    return render(request, 'invoice.html', ctx)

def contract(request):
    profile = request.user.profile
    utility = Utility.objects.get(user = request.user)
    day = datetime.datetime.now()
    ctx = {
        "profile": profile,
        "day": day.strftime("%d"),
        "month": day.strftime("%B"),
        "year": day.strftime("%Y"),
        "utility": utility,
    }

    if request.method == "POST":
        supplierSignature = request.POST.get("suppliersignInput")
        consumerSignature = request.POST.get("consumersignInput")

        contract = Contract(user = utility.user.profile, provider = utility.supplier, consumersignature = consumerSignature, suppliersignature = supplierSignature)
        contract.save()

        # try:
        #     contract = Contract(user = utility.user.profile, provider = utility.supplier, consumersignature = consumerSignature, suppliersignature = supplierSignature)
        #     contract.save()
        # except:
        #     print("already have contract")
        #     print(Exception)

    return render(request, 'contract.html', ctx)

def paymentDetails(request):
    return render(request, 'paymentDetails.html')

def ProfilePage(request):
    contract = 0
    try:
        user = User.objects.get(username = request.user)
        contract = Contract.objects.get(user = request.user.profile)
        print(contract)
    except:
        print("no contract information")

    if (request.method == "POST"):
        print("req")
    return render(request, 'profile.html', {"user": user, "contract": contract})

def backupPage(request):
    # sysout = sys.stdout
    # sys.stdout = open("data2.json", "w")
    # management.call_command("dumpdata", "base")
    # sys.stdout = sysout
    prs = subprocess.run('python manage.py dumpdata --indent 4 > newdata.json', shell=True)
    print("status :", prs.returncode)
    return render(request, 'backup.html')

def payment(request):
    
    encoded_credentials = base64.b64encode(f"{settings.MPESA_CONSUMER_KEY}:{settings.MPESA_CONSUMER_SECRET}".encode('utf-8')).decode('utf-8')
    get_token = requests.get("https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials", headers={"Authorization": f"Basic {encoded_credentials}"})
    print(get_token.status_code)
    token = get_token.json()['access_token']
    
    url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    headers = {
        "Authorization" : f"Bearer {token}",
        "Content-Type" : "application/json"
    }

    def generatepassword(passkey, shortcode):
        timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        hashdata = shortcode + passkey + timestamp
        encoded_password = base64.b64encode(hashdata.encode()).decode('utf-8')
        return encoded_password

    payload = {
        "BusinessShortCode" : settings.MPESA_SHORTCODE,
        "Password" : generatepassword(settings.MPESA_PASSKEY, settings.MPESA_SHORTCODE),
        "Timestamp" : datetime.datetime.now().strftime('%Y%m%d%H%M%S'),
        "TransactionType": "CustomerPayBillOnline",
        "Amount" : "1",
        "PartyA" : "254708323035",
        "PartyB" : settings.MPESA_SHORTCODE,
        "PhoneNumber" : "254708323035",
        "CallBackURL" : "https://20d8-41-215-18-254.ngrok-free.app/paymentcallback/",
        "AccountReference" : settings.MPESA_INITIATOR_USERNAME,
        "TransactionDesc" : "water payment"
    }

    response = requests.post(url, json=payload, headers=headers)
    response_json = response.json()
    print(response_json)
    
    return HttpResponse(response_json)

@csrf_exempt
def paymentcallback(request):
    if request.method == "POST":
        print(request.body)
    return HttpResponse(status=200)