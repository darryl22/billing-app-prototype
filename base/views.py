from django.shortcuts import render
from .models import Utility, Reading
import plotly.express as px

# Create your views here.

def home(request):
    return render(request, 'home.html')

def login(request):
    return render(request, 'login.html')

def signup(request):
    return render(request, 'signup.html')

def dashboard(request):
    
    return render(request, 'dashboard.html')

def UtilityDetails(request, pk):
    data = []
    utility = Utility.objects.get(name = pk)
    readings = Reading.objects.filter(utility = utility)
    for x in readings:
        data.append(x.reading)
    print(data)

    fig = px.line(
        x = ["date 1", "date 2", "date 3", "date 4", "date 5"],
        y = data,
        title = "meter readings",
        markers = True,
        labels = {
            "x": "dates",
            "y": "values",
            "variable": "utilities"
        }
    )
    line = fig.to_html()

    ctx = {
        "utility": utility,
        "redings": readings,
        "line": line
    }
    return render(request, 'utilityDetails.html', ctx)