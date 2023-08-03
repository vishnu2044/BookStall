from django.shortcuts import render, redirect, get_object_or_404
from .models import Cart, CartItem
from app_products.models import Product
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from app_offer.models import *

# Create your views here.
def _session_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


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

def cart(request, total=0, quantity=0, cart_items=None, count=0, discount_amount=0, cart=None, coupons=None, subtotal=0, og_total=0,discount_amnt=0):
    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user)
        else:
            cart = Cart.objects.get(session_id=_session_id(request))
            cart_items = CartItem.objects.filter(cart=cart)

        for cart_item in cart_items:
            og_total += cart_item.sub_total()
            if cart_item.product.offer:
                total += cart_item.sub_total_with_offer()
            elif cart_item.product.category.offer:
                total += cart_item.sub_total_with_category_offer()
            else:
                total += cart_item.sub_total()

            quantity += cart_item.quantity
            count += 1
            subtotal = total
            discount_amnt = og_total - total
            
        print("*")
        

    except CartItem.DoesNotExist:
        # Handle the case where no cart items exist for the user or session
        cart_items = None

    except Cart.DoesNotExist:
        # Handle the case where no cart exists for the session
        cart_items = None


    #adding coupons 
    if request.method == "POST":
        coupon_obj = request.POST.get("search")
        try:
            coupon = Coupon.objects.get(coupon_code = coupon_obj)
            if coupon.is_expired():
                messages.error(request, 'coupon is expaired')
                return redirect('cart')
            if coupon.min_amount > total:
                messages.error(request, f'Amount should be greater than {coupon.min_amount}')
                return redirect('cart')
            discount_amount = total * coupon.off_percent / 100

            cart = Cart.objects.get(session_id= _session_id(request))
            if discount_amount > coupon.max_discount:
                discount_amount = coupon.max_discount

            subtotal = total
            total -= discount_amount
            cart.coupon = coupon
            cart.save()
            cart_item.coupon_discount = discount_amount
            cart_item
            coupon.coupon_stock -= 1
            coupon.save()
        except:
            messages.error(request, 'coupon not found')



    context = {
        "discount_amnt": discount_amnt,
        "og_total": og_total,
        "total": total,
        "quantity": quantity,
        "cart_items": cart_items,
        "count": count,
        "coupons": coupons,
        "cart": cart,
        "discount_amount": discount_amount,
        "sub_total": subtotal,
    }

    return render(request, "temp_home/cart.html", context)


