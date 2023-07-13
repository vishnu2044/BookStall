from django.shortcuts import render, redirect
from app_cart.models import *
from app_accounts.models import UserAddress
from .models import *
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings

# Create your views here.
def payments(request):
    if request.user.is_authenticated:
        payment_method = PaymentMethod.objects.get(id=1)
        payment = Payment(
            user = request.user,
            payment_method = payment_method,
        )
        payment.save()
        order = Order.objects.filter(user=request.user).order_by('-id').first()
        order.payment = payment
        order.status = 'accepted'
        order.save()
    
        # move the cart items into ordered items
        cart_items = CartItem.objects.filter(user=request.user)
        orderitem = None
        for cart_item in cart_items:
            if orderitem is None:
                orderitem = OrderItem(
                    user = request.user,
                    order = order,
                    product = cart_item.product,
                    product_price = cart_item.product.price,
                    quantity = cart_item.quantity,
                    status = 'accepted',
                )
            else:
                orderitem.quantity += cart_item.quantity
            orderitem.save()

        #reduce the stock of ordered product.
            product = cart_item.product
            product_name = product.product_name
            product.stock -= cart_item.quantity
            product.save()

        CartItem.objects.filter(user=request.user).delete()

        mess = f'Hello\t{request.user.first_name} {request.user.last_name} \nYour order of { product_name} has confirmed.\n Thanks!'

        send_mail(
            "Thank you\n",
            mess,
            settings.EMAIL_HOST_USER,
            [request.user.email],
            fail_silently=False,
        )
        return render(request, 'temp_home/confirm.html')
    return redirect(request, 'place_order')

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
            total += ((cart_item.product.price) * (cart_item.quantity))
        if cart_count <= 0:
            return redirect('home')

        if request.method == "POST":
            addr = request.POST["address"]
            address = UserAddress.objects.get(id=addr)
        else:
            address = UserAddress.objects.filter(user=current_user).first()

        data = Order()
        data.user = current_user
        data.address = address
        data.order_total = total
        data.save()
        order = Order.objects.get(user = current_user, status = data.status, order_id = data.order_id, order_total = data.order_total)

        context = {
            'order' : order,
            'cart_items' : cart_items,
        }
        return render(request, 'temp_home/payments.html', context)
    return redirect(request, '/')

    



















    

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


            