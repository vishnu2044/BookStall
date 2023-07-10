from django.shortcuts import render
from app_products.models import *
# Create your views here.

def home(request):
    products = Product.objects.all().filter(is_available=True)
    context = {
        "products_slides": products[3:],
        "products": products[:3],
        "popular_products" : products[:6],
        
    }
    return render(request, "temp_home/home.html",context)

def base(request):
    return render(request, "temp_home/base.html")
 
def about(request):
    return render(request, "temp_home/about.html")
 
 
def shop(request):
    products = Product.objects.all().filter(is_available=True)
    context = {
        "products": products[:3],
        "products_new_araivals" : products[:3],
        "products_old_books" : products[3:],
        "products_popular" : products[2:5],
        
    }
    return render(request, 'temp_home/shop.html', context)


def product_details(request, id):
    product = Product.objects.get(id=id)
    context = {
        "product": product,
    }
    return render(request, 'temp_home/product_details.html', context)