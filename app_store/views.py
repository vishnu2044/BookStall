from django.shortcuts import render, redirect
from app_products.models import *
from app_cart.models import CartItem
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from app_authors.models import *
# Create your views here.
def shop(request):
  
    products = Product.objects.all().filter(is_available=True)
    cart_items = CartItem.objects.all()

   

    authors = Authors.objects.all()
    categories = Category_list.objects.all()

    #filtering products
    price_range = request.GET.get('price_range')
    category = request.GET.get('category')
    author = request.GET.get('author')

    if price_range:
        min_price , max_price = map(int, price_range.split("-"))
        products = Product.objects.filter(price__gte = min_price, price__lte = max_price)

    if category:
        categ = Category_list.objects.filter(category_name = category)
        products = Product.objects.filter(category = categ)

    if author:
        author_filter = Authors.objects.filter(author_name = author)
        products = Product.objects.filter(author = author_filter)


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
        "authors": authors,
        "categories": categories,
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
    products = Product.objects.filter(product_name__icontains=search_text)

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
        "search_text" : search_text,
    }
    return render(request, 'temp_home/shop.html', context)
    

def filtering_products(request):
    products = Product.objects.filter(is_available=True)
    authors = Authors.objects.all()
    categories = Category_list.objects.all()

    # Filtering products
    price_range = request.GET.get('price_range')
    category = request.GET.get('category')
    author = request.GET.get('author')

    if price_range:
        min_price, max_price = map(int, price_range.split("-"))
        products = products.filter(price__gte=min_price, price__lte=max_price)

    if category:
        try:
            category_obj = Category_list.objects.get(category_name=category)
            products = products.filter(category=category_obj)
        except Category_list.DoesNotExist:
            pass

    if author:
        try:
            author_obj = Authors.objects.get(author_name=author)
            products = products.filter(author=author_obj)
        except Authors.DoesNotExist:
            pass

    per_page = 6
    page_number = request.GET.get('page')
    paginator = Paginator(products, per_page)

    try:
        current_page = paginator.page(page_number)
    except PageNotAnInteger:
        current_page = paginator.page(1)
    except EmptyPage:
        current_page = paginator.page(paginator.num_pages)

    context = {
        "current_page": current_page,
        "authors": authors,
        "categories": categories,
        "products": products,
    }

    return render(request, 'temp_home/shop.html', context)


def sorting_products(request):
    products = Product.objects.filter(is_available=True)

    a_to_z = request.GET.get('a-z')
    z_to_a = request.GET.get('z-a')
    high_to_low = request.GET.get('high_to_low')
    low_to_high = request.GET.get('low_to_high')

    if a_to_z:
        products = Product.objects.all().order_by('product_name')

    if z_to_a:
        products = Product.objects.all().order_by('-product_name')

    if high_to_low:
        products = Product.objects.all().order_by('price')

    if low_to_high:
        products = Product.objects.all().order_by('-price')

    per_page = 6
    page_number = request.GET.get('page')
    paginator = Paginator(products, per_page)

    try:
        current_page = paginator.page(page_number)
    except PageNotAnInteger:
        current_page = paginator.page(1)
    except EmptyPage:
        current_page = paginator.page(paginator.num_pages)

    context = {
        "current_page": current_page,
        "products": products,
    }

    return render(request, 'temp_home/shop.html', context)