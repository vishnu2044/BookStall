from django.shortcuts import render
from app_products.models import Product
# Create your views here.

def home(request):
    products = Product.objects.all().filter(is_available=True)
    context = {
        "products": products[3:]
    }
    return render(request, "temp_home/home.html",context)

def base(request):
    return render(request, "temp_home/base.html")
 
def about(request):
    return render(request, "temp_home/about.html")
 
def shop(request):
    return render(request, 'temp_home/shop.html')