from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, "temp_home/home.html")

def base(request):
    return render(request, "temp_home/base.html")
 
def about(request):
    return render(request, "temp_home/about.html")
 
def shop(request):
    return render(request, 'temp_home/shop.html')