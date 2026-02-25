from django.shortcuts import render,HttpResponse
from home.models import Contact
from home.models import Feedback

# Create your views here.
def index(request):
    context={'variable':"this is sent"}
    return render(request,'index.html',context)
def about(request):
    return render(request,'about.html')

def services(request):
    return render(request,'services.html')

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