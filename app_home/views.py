from django.shortcuts import render
from app_products.models import *
from app_cart.models import CartItem
# Create your views here.

def home(request):
    products = Product.objects.all().filter(is_available=True)
    authors = Authors.objects.all()
    context = {
        "products_slides": products[3:],
        "products": products[:3],
        "popular_products" : products[:6],
        "authors" : authors,
  
    }
    return render(request, "temp_home/home.html",context)

def base(request):
    return render(request, "temp_home/base.html")
 
def about(request):
    return render(request, "temp_home/about.html")
 
 
def shop(request):
  
    products = Product.objects.all().filter(is_available=True)
    cart_items = CartItem.objects.all()
    
    context = {
        "products": products[:3],
        "products_new_araivals" : products,
        "products_old_books" : products[3:],
        "products_popular" : products[2:5], 
        "cart_items" : cart_items,
    }
    
    return render(request, 'temp_home/shop.html', context)


def product_details(request, id):
    product = Product.objects.get(id=id)
    context = {
        "product": product,
    }
    return render(request, 'temp_home/product_details.html', context)
