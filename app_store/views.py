from django.shortcuts import render
from app_products.models import *
from app_cart.models import CartItem
# Create your views here.
def shop(request):
  
    products = Product.objects.all().filter(is_available=True)
    cart_items = CartItem.objects.all()
    
    context = {
        "products": products,
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

def product_search(request):
    search_text = request.POST.get("query")
    products = Product.objects.filter(product_name__icontains = search_text)
    context = {
        "products": products,
        "search_text" : search_text,
    }
    return render(request, 'temp_home/shop.html', context)