from django.shortcuts import render, redirect
from .models import Utility, Reading, Profile
from django.contrib import messages
from django.contrib.auth.models import User
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

        if password == confirmpassword:
            user = User.objects.create_user(username, email, password)
            user.save()
            profile = Profile(user = user, name = user.username, usertype = usertype, nationalID = nationalID, address = address, phone = phone)
            profile.save()
            login(request, user)
            return redirect("dashboard")
        else:
            messages.error(request, "passwords did not match")
    return render(request, 'signup.html')

def logoutUser(request):
    logout(request)
    return redirect('main')

def dashboard(request):
    ctx = []
    if request.user.is_authenticated:
        utility = Utility.objects.filter(user = request.user)
        for x in utility:
            ctx.append(x)
    
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
    utility = Utility.objects.filter(user = request.user).get(name = pk)
    readings = Reading.objects.filter(utility = utility)
    for x in readings:
        data.append(x.reading)
        labels.append(x.created)
    
    unit = utility.unit

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
        height = 580,
        width = 1000
    )
    line = fig.to_html()

    ctx = {
        "utility": utility,
        "readings": readings,
        "line": line,
        "unit": unit
    }
    return render(request, 'utilityDetails.html', ctx)

def invoice(request, pk):
    data = []
    labels = []
    utility = Utility.objects.filter(user = request.user).get(name = pk)
    readings = Reading.objects.filter(utility = utility)
    for x in readings:
        data.append(x.reading)
        labels.append(x.created)
    print(data)
    consumed = data[-1] - data[-2]
    consumedAmount = consumed * 100
    month = datetime.datetime.now()

    ctx = {
        "utility": utility,
        "current": data[-1],
        "previous": data[-2],
        "consumed": consumed,
        "consumedAmount": consumedAmount,
        "month": month.strftime("%B"),
        "day": month.strftime("%d"),
        "year": month.strftime("%Y")
    }
    return render(request, 'invoice.html', ctx)

def contract(request):
    return render(request, 'contract.html')