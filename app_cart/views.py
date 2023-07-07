from django.shortcuts import render, redirect

# Create your views here.
def cart(request):
    return render(request, "temp_home/cart.html")