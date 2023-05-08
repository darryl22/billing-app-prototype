from django.shortcuts import render, redirect
from .models import Utility, Reading, Profile
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
import plotly.express as px
import datetime

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
    print(request.user.profile.usertype)
    if request.user.is_authenticated:
        if request.user.profile.usertype == "supplier":
            utility = Utility.objects.all()
            for x in utility:
                ctx.append(x)
        else:
            utility = Utility.objects.filter(user = request.user)
            for x in utility:
                ctx.append(x)
            
    print(ctx)
    if request.method == "POST":
        reading = request.POST.get("reading")
        utilId = request.POST.get("utility")
        util = Utility.objects.get(id = utilId)
        print(reading, utility)
        r = Reading(utility = util, reading = reading)
        r.save()
    
    return render(request, 'dashboard.html', {"data": ctx, "length": len(ctx)})

def UtilityDetails(request, pk):
    data = []
    labels = []
    dif = []
    amount = []
    utility = Utility.objects.filter(user = request.user).get(name = pk)
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
    x = list(zip(data, dif, labels, amount))

    ctx = {
        "utility": utility,
        "line": line,
        "unit": unit,
        "data": x
    }
    return render(request, 'utilityDetails.html', ctx)

def invoice(request, pk):
    data = []
    labels = []
    profile = Profile.objects.get(name = request.user)
    arrears = int(profile.arrears)
    print(arrears)
    utility = Utility.objects.filter(user = request.user).get(name = pk)
    readings = Reading.objects.filter(utility = utility)
    for x in readings:
        data.append(x.reading)
        labels.append(x.created)
    consumed = data[-1] - data[-2]
    consumedAmount = consumed * utility.rate
    day = datetime.datetime.now()

    ctx = {
        "utility": utility,
        "current": data[-1],
        "previous": data[-2],
        "consumed": consumed,
        "consumedAmount": consumedAmount,
        "amountpayable": consumedAmount + arrears,
        "month": day.strftime("%B"),
        "day": day.strftime("%d"),
        "year": day.strftime("%Y"),
        "profile": profile,
        "arrears": arrears
    }
    return render(request, 'invoice.html', ctx)

def contract(request, pk):
    profile = request.user.profile
    utility = Utility.objects.filter(user = request.user).get(name = pk)
    day = datetime.datetime.now()
    ctx = {
        "profile": profile,
        "day": day.strftime("%d"),
        "month": day.strftime("%B"),
        "year": day.strftime("%Y"),
        "utility": utility,
    }

    return render(request, 'contract.html', ctx)

def paymentDetails(request):
    return render(request, 'paymentDetails.html')

def ProfilePage(request):
    user = User.objects.get(username = request.user)
    print(user)
    return render(request, 'profile.html', {"user": user})