from django.shortcuts import render, redirect
from app_cart.models import *
from app_accounts.models import UserAddress
from .models import *
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
import razorpay

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
            product = Product.objects.get(id=cart_item.product.id)
            product.stock -= cart_item.quantity
            product.save()

        CartItem.objects.filter(user=request.user).delete()

        # mess = f'Hello\t{request.user.first_name} {request.user.last_name} \nYour order of { product_name} has confirmed.\n Thanks!'

        # send_mail(
        #     "Thank you for your order",
        #     mess,
        #     settings.EMAIL_HOST_USER,
        #     [request.user.email],
        #     fail_silently=False,
        # )

        CartItem.objects.filter(user=request.user).delete()

        order = Order.objects.filter(user=request.user).order_by('-id').first()
        order_item = OrderItem.objects.filter(user=request.user)

        context = {
            "order": order,
            "order_items": order_item,
        }
        

        return render(request, 'temp_home/confirm.html', context)

    return redirect(place_order)

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

        client = razorpay.Client(auth=( settings.KEY_ID, settings.KEY_SECRET ))
        payment = client.order.create({"amount" : total * 100, 'currency': "INR", "payment_capture" : 1})

        context = {
            'order' : order,
            'cart_items' : cart_items,
            "payment" : payment,
        }
        return render(request, 'temp_home/payments.html', context)
    return redirect(request, '/')


def payment_success(request,):
    if request.user.is_authenticated:
        payment_method = PaymentMethod.objects.get(id=2)
        payment = Payment(
            user = request.user,
            payment_method = payment_method,
            status = 'paid'
        )
        payment.save()
        order = Order.objects.filter(user=request.user).order_by('-id').first()
        order.status = 'accepted'
        order.save()
        cart_items = CartItem.objects.filter(user = request.user)

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
            product = Product.objects.get(id=cart_item.product.id)
            product.stock -= cart_item.quantity
            product.save()

        CartItem.objects.filter(user=request.user).delete()

        order = Order.objects.filter(user=request.user).order_by('-id').first()
        order_item = OrderItem.objects.filter(user=request.user)

        context = {
            "order": order,
            "order_items": order_item,
        }
            

        return render(request, 'temp_home/confirm.html', context)
    return redirect(place_order)


def add_user_address(request):
    if request.method == "POST":
        name = request.POST.get("name")
        ph_no = request.POST.get("number")
        house = request.POST.get("house")
        landmark = request.POST.get("landmark")
        district = request.POST.get("district")
        city = request.POST.get("city")
        state = request.POST.get("state")
        country = request.POST.get("country")
        pincode = request.POST.get("pincode")
        
        UserAddress.objects.create(
            fullname = name,
            contact_number = ph_no,    
            user = request.user,
            house_name = house,
            landmark = landmark,
            city = city,
            district = district,
            state = state,
            country = country,
            pincode = pincode,
        ).save()
        return redirect('place_order')

def user_order_list(request):
    order_items = OrderItem.objects.filter(user = request.user)

    context  ={
        "order_items" : order_items,
    } 
    return render(request, 'temp_home/user_order_list.html', context)
    


def user_order_cancel(request, id):
    order_item = OrderItem.objects.get(id=id)
    if order_item.status == "accepted":
        order_item.status = "Cancelled"
        order_item.save()
        return redirect(user_order_list , pk=id)
    
    order_items = OrderItem.objects.filter(user = request.user)

    context  ={
        "order_items" : order_items,
    } 
    return render(request, 'temp_home/user_order_list.html', context)



















    

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


            