from django.urls import path
from base import views

urlpatterns = [
    path('', views.home, name="main"),
    path('login/', views.login, name="login"),
    path('signup/', views.signup, name="signup"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('utilityDetails/<str:pk>/', views.UtilityDetails, name="utilityDetails"),
]