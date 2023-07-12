from django.shortcuts import render, redirect
from app_cart.models import *
from app_accounts.models import UserAddress
from .models import *

# Create your views here.

def place_order(request):
    if request.user.is_authenticated:
        current_user = request.user
        total = 0
        cart_items = CartItem.objects.filter(user = current_user)
        cart_count = cart_items.count()
        for cart_item in cart_items:
            if cart_item.quantity > cart_item.product.stock:
                print("cart item out of stock")
                return redirect('cart')
            total += ((cart_item.product.price)*(cart_item.quantity))
        if cart_count <= 0:
            return redirect('home')
        
        if request.method == "POST":
            addr = request.POST.get('address')
            address = UserAddress.objects.get(id=addr)
        else:
            address = UserAddress.objects.filter(user=current_user).order_by('id').first()

        data = Order()
        data.user = current_user
        data.address = address
        data.order_total = total
        data.save()
        order = Order.objects.get(user = current_user, status = data.status, order_id = data.order_id)

        context = {
            'order' : order,
            'cart_items' : cart_items,
        }
        return render(request, 'temp_home/payments.html', context)
    

















    

# def place_order(request):
#     if request.user.is_authenticated:
#         current_user = request.user
#         total = 0
#         cart_items = CartItem.objects.filter(user=current_user)
#         cart_count = cart_items.count()
#         for cart_item in cart_items:
#             if cart_item.quantity > cart_item.product.stock:
#                 print("cart item out of stock")
#                 return redirect('cart')
#             total += ((cart_item.product.price) * (cart_item.quantity))
#         if cart_count <= 0:
#             return redirect('home')

#         if request.method == "POST":
#             address_id = request.POST.get("address_id")
#             if not address_id:
#                 raise ValueError("Address ID is not set")

#             address = UserAddress.objects.get(id=address_id)

#             data = Order()
#             data.user = current_user
#             data.address = address
#             data.order_total = total
#             data.save()
#             order = Order.objects.get(user=current_user, status=data.status, order_id=data.order_id)

#             context = {
#                 'order': order,
#                 'cart_items': cart_items,
#             }
#             return render(request, 'temp_home/payments.html', context)
#         else:
#             address = UserAddress.objects.filter(user=current_user).order_by('id').first()

#             data = Order()
#             data.user = current_user
#             data.address = address
#             data.order_total = total
#             data.save()
#             order = Order.objects.get(user=current_user, status=data.status, order_id=data.order_id)

#             context = {
#                 'order': order,
#                 'cart_items': cart_items,
#             }
#             return render(request, 'temp_home/payments.html', context)

#     else:
#         return redirect('login')


            