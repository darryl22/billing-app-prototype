from django.shortcuts import render, redirect
from .models import Utility, Reading
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
import plotly.express as px

# Create your views here.

def home(request):
    return render(request, 'home.html')

def loginUser(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            user = User.objects.get(username = username)
        except:
            messages.error(request, "user not found")
        
        user = authenticate(request, username = username, password = password)

        if user is not None:
            login(request, user)
            return redirect("dashboard")
        else:
            messages.error(request, "invalid login credentials")

    return render(request, 'login.html')

def signup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirmpassword = request.POST.get("confirm-password")

        if password == confirmpassword:
            user = User.objects.create_user(username, email, password)
            user.save()
            login(request, user)
            return redirect("dashboard")
        else:
            messages.error(request, "passwords did not match")
    return render(request, 'signup.html')

def logoutUser(request):
    logout(request)
    return redirect('main')

def dashboard(request):
    
    return render(request, 'dashboard.html')

def UtilityDetails(request, pk):
    data = []
    labels = []
    utility = Utility.objects.get(name = pk)
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
        "redings": readings,
        "line": line,
        "unit": unit
    }
    return render(request, 'utilityDetails.html', ctx)