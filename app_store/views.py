from django.shortcuts import render
from app_products.models import *
from app_cart.models import CartItem
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.
def shop(request):
  
    products = Product.objects.all().filter(is_available=True)
    cart_items = CartItem.objects.all()

    per_page = 6
    page_number = request.GET.get('page')
    paginator = Paginator(products, per_page)

    try:
        current_page = paginator.page(page_number)
    
    except PageNotAnInteger:
        # If the 'page' parameter is not an integer, display the first page
        current_page = paginator.page(1)

    except EmptyPage:
        current_page = paginator.page(paginator.num_pages)

    
    context = {
        "current_page": current_page,
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