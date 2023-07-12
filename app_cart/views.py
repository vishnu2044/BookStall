from django.shortcuts import render, redirect, get_object_or_404
from .models import Cart, CartItem
from app_products.models import Product
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
def _session_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def add_cart(request, product_id):
    product = Product.objects.get(id = product_id)
    try:
        cart = Cart.objects.get(session_id = _session_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            session_id = _session_id(request)
        )
    cart.save()

    try:
        cart_item = CartItem.objects.get(product=product, cart = cart)
        if ((product.stock)-(cart_item.quantity + 1)) < 0:
            print("asd")
            return redirect('cart')
        
        cart_item.quantity +=1
        cart_item.save()
    except CartItem.DoesNotExist:
        if request.user.is_authenticated:
            if ((product.stock) - 1) <0:
                print("asd")
                return redirect(request, 'cart')
            
            cart_item = CartItem.objects.create(
                product = product,
                quantity=1,
                cart = cart,
                user = request.user,
            )
            cart_item.save()
        else:
            cart_item = CartItem.objects.create(
                product=product,
                quantity =1,
                cart = cart,
            )
            cart_item.save()
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

    context = {
        "total": total,
        "quantity": quantity,
        "cart_items": cart_items,
        "count": count,
    }

    return render(request, "temp_home/cart.html", context)
