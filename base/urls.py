from django.urls import path
from base import views

urlpatterns = [
    path('', views.home, name="main"),
    path('login/', views.loginUser, name="login"),
    path('signup/', views.signup, name="signup"),
    path('logout/', views.logoutUser, name="logout"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('utilityDetails/<str:pk>/', views.UtilityDetails, name="utilityDetails"),
    path('invoice/', views.invoice, name="invoice"),
    path('contract/', views.contract, name="contract"),
    path('paymentDetails/', views.paymentDetails, name="paymentDetails"),
    path('profile/', views.ProfilePage, name="profile"),
    path('backup/', views.backupPage, name="backup"),
    path('payment/', views.payment, name="payment"),
    path('paymentcallback/<str:pk>', views.paymentcallback, name="paymentcallback"),
]