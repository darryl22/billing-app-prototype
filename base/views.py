from django.shortcuts import render, redirect
from .models import Utility, Reading, Profile, Contract, Invoice
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
import plotly.express as px
from django.http import HttpResponse
from django_daraja.mpesa.core import MpesaClient
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
                print(x.reading_set.latest("created"))
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

        day = datetime.datetime.now()
        reading = float(request.POST.get("reading"))
        utilId = request.POST.get("utility")
        util = Utility.objects.get(id = utilId)
        latest_reading = Reading.objects.filter(utility = util).latest("created")
        profile = Profile.objects.get(user = util.user)
        amount = round(((reading - latest_reading.reading) * util.rate), 2)

        if profile.prepayment >= amount:
            newprepayment = profile.prepayment - amount
            profile.prepayment = newprepayment
            profile.save()

            invoice = Invoice(
                user = util.user,
                billingmonth = day.strftime("%B"),
                year = day.strftime("%Y"), 
                previousreading = latest_reading.reading,
                currentreading = reading,
                consumed = round((reading - latest_reading.reading), 2),
                rate = util.rate,
                consumptionamount = amount,
                arrears = profile.arrears,
                prepayment = profile.prepayment,
                amountpayable = profile.arrears
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
                billingmonth = day.strftime("%B"),
                year = day.strftime("%Y"),
                previousreading = latest_reading.reading,
                currentreading = reading,
                consumed = round((reading - latest_reading.reading), 2),
                rate = util.rate,
                consumptionamount = amount,
                arrears = prevarrears,
                prepayment = profile.prepayment,
                amountpayable = newarrears
                )
            invoice.save()

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
    try:
        invoice = Invoice.objects.filter(user = request.user).latest("created")
        print(invoice.created)
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

def contract(request):
    profile = request.user.profile
    day = datetime.datetime.now()
    ctx = {
        "profile": profile,
        "day": day.strftime("%d"),
        "month": day.strftime("%B"),
        "year": day.strftime("%Y"),
    }

    if request.method == "POST":
        supplierSignature = request.POST.get("suppliersignInput")
        consumerSignature = request.POST.get("consumersignInput")

        contract = Contract(user = request.user, consumersignature = consumerSignature, suppliersignature = supplierSignature)
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
    
    cl = MpesaClient()
    token = cl.access_token()
    phone = "0708323035"
    amount = 1
    account_reference = "test"
    transaction_desc = "billing payment"
    callback_url = f"https://ecf2-41-215-18-254.ngrok-free.app/paymentcallback/{request.user.username}"

    response = cl.stk_push(phone, amount, account_reference, transaction_desc, callback_url)
    print(response.customer_message)
    print(response.response_code)
    print(response.content)
    print(response.json())
    return HttpResponse(response)

@csrf_exempt
def paymentcallback(request, pk):
    profile = Profile.objects.get(name = pk)
    print(profile.arrears)

    if request.method == "POST":
        res = request.body.decode("utf-8")
        res_obj = eval(res)
        callbackdata = res_obj['Body']['stkCallback']
        print(callbackdata)
        if callbackdata['ResultCode'] == 0:
            print("successfull payment")
            amount = callbackdata['CallbackMetadata']['Item'][0]['Value']
            receiptnumber = callbackdata['CallbackMetadata']['Item'][1]['Value']
            print("amount", amount)
            print("receipt number", receiptnumber)
        else:
            print("error with payment process")
    return HttpResponse(status=200)