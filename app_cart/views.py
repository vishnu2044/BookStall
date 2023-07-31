from django.shortcuts import render, redirect, get_object_or_404
from .models import Cart, CartItem
from app_products.models import Product
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages

# Create your views here.
def _session_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

from django.contrib import messages

def add_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart, created = Cart.objects.get_or_create(session_id=_session_id(request))

    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        updated_quantity = cart_item.quantity + 1
        if updated_quantity > product.stock:
            messages.warning(request, "Sorry, this product is out of stock.")
        else:
            cart_item.quantity = updated_quantity
            cart_item.save()
    except CartItem.DoesNotExist:
        if request.user.is_authenticated:
            if product.stock < 1:
                messages.warning(request, "Sorry, this product is out of stock.")
            else:
                CartItem.objects.create(
                    product=product,
                    quantity=1,
                    cart=cart,
                    user=request.user,
                )
        else:
            if product.stock < 1:
                messages.warning(request, "Sorry, this product is out of stock.")
            else:
                CartItem.objects.create(
                    product=product,
                    quantity=1,
                    cart=cart,
                )
    
    return redirect('cart')


def remove_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(product=product, user=request.user)
    else:
        cart = Cart.objects.get(session_id = _session_id(request))
        cart_item = CartItem.objects.get(product=product, cart = cart)
    if cart_item.quantity >1:
        cart_item.quantity -=1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')



def delete_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(product=product, user=request.user)
    else:
        cart = Cart.objects.get(session_id=_session_id(request))
        cart_items = CartItem.objects.filter(product=product, cart=cart)

    cart_items.delete()
    return redirect('cart')

def cart(request, total=0, quantity=0, cart_items=None, count=0):
    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user)
        else:
            cart = Cart.objects.get(session_id=_session_id(request))
            cart_items = CartItem.objects.filter(cart=cart)

        for cart_item in cart_items:
            total += cart_item.sub_total()
            quantity += cart_item.quantity
            count += 1

    except CartItem.DoesNotExist:
        # Handle the case where no cart items exist for the user or session
        cart_items = None

    except Cart.DoesNotExist:
        # Handle the case where no cart exists for the session
        cart_items = None


    #adding coupons 
    


    context = {
        "total": total,
        "quantity": quantity,
        "cart_items": cart_items,
        "count": count,
    }

    return render(request, "temp_home/cart.html", context)
