from django.shortcuts import render, redirect
from app_cart.models import *
from app_accounts.models import UserAddress

# Create your views here.
def checkout(request):
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
        for cart_item in cart_items:
            if cart_item.quantity > cart_item.product.stock:
                print("cart item out of stock")
                return redirect('cart')
        address = UserAddress.objects.filter(user=request.user)
        context = {
            'addresses': address
        }
    return render(request, 'temp_home/checkout.html', context)