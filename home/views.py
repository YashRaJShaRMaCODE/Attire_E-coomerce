from django.shortcuts import render,HttpResponse
from home.models import Contact
from home.models import Feedback
from django.contrib.auth import authenticate, login, logout
# Create your views here.
def index(request):
    context={'variable':"this is sent"}
    return render(request,'index.html',context)
def about(request):
    return render(request,'about.html')

def services(request):
    return render(request,'services.html')
def profile_settings(request):
    return render(request, 'profile_settings.html')

def account_settings(request):
    return render(request, 'account_settings.html')

def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')


        Contact.objects.create(
            name=name,
            email=email,
            message=message
        )

    return render(request, 'contact.html')

def feedback(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')


        Feedback.objects.create(
            name=name,
            email=email,
            message=message
        )
    return render(request,'feedback.html')
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "login.html")


def user_logout(request):
    logout(request)
    return redirect('login')

def cart(request):
    return render(request, 'cart.html')
def my_account(request):
    return render(request, 'my_account.html')   

def profile_setting(request):
    return render(request, 'profile_setting.html')  
def account_setting(request):   
    return render(request, 'account_setting.html')
def my_orders(request):
    return render(request, 'my_orders.html')    
def saved_addresses(request):
    return render(request, 'saved_addresses.html')
def settings(request):
    return render(request, 'settings.html')
def purchase_history(request):
    return render(request, 'purchase_history.html')