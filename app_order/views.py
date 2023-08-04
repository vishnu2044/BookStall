from django.shortcuts import render, redirect
from app_cart.models import *
from app_accounts.models import UserAddress
from .models import *
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
import razorpay
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
def _session_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart  

# payment for cashon delivery 
def payments(request, total=0, ):
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
        for cart_item in cart_items:
            product_price = 0
            if cart_item.product.offer:
                product_price = cart_item.product.get_offer_price()
            if cart_item.product.category.offer:
                product_price = cart_item.product.get_offer_price_by_category()
            else:
                product_price = cart_item.product.price

            orderitem = OrderItem(
                user = request.user,
                order = order,
                product = cart_item.product,
                product_price = product_price,
                quantity = cart_item.quantity,
                status = 'accepted',
            )
            orderitem.save()

            total += orderitem.sub_total()


        #reduce the stock of ordered product.
            product = Product.objects.get(id=cart_item.product.id)
            product.stock -= cart_item.quantity
            product.save()
        print("*******************", total, "******************************")
        cart = Cart.objects.get(session_id=_session_id(request))
        discount_amount = total * cart.coupon.off_percent / 100
        if discount_amount > cart.coupon.max_discount:
            discount_amount = cart.coupon.max_discount
        if discount_amount:
            total -= discount_amount
        print("*******************************************", discount_amount,"****************************")

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
            "total": total,
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
        og_total = 0
        for cart_item in cart_items:
            if cart_item.quantity > cart_item.product.stock:
                print("cart item out of stock")
                return redirect('cart')
            og_total += cart_item.sub_total()
            if cart_item.product.offer:
                total += cart_item.sub_total_with_offer()
            elif cart_item.product.category.offer:
                total += cart_item.sub_total_with_category_offer()
            else:
                total += cart_item.sub_total()
        
        cart = Cart.objects.get(session_id=_session_id(request))
        discount_amount = 0
        if cart.coupon:
            discount_amount = total * cart.coupon.off_percent / 100
            if discount_amount > cart.coupon.max_discount:
                discount_amount = cart.coupon.max_discount
            total -= discount_amount

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
        data.discount_amount = discount_amount
        data.save()
        order = Order.objects.get(user = current_user, 
                                  status = data.status, 
                                  order_id = data.order_id, 
                                  order_total = data.order_total
                                )

        client = razorpay.Client(auth=( settings.KEY_ID, settings.KEY_SECRET ))
        payment = client.order.create({"amount" : total * 100, 'currency': "INR", "payment_capture" : 1})

        context = {
            'total' : total,
            'og_total' : og_total,
            'discount_amount' : discount_amount,
            'order' : order,
            'cart_items' : cart_items,
            "payment" : payment,
        }
        return render(request, 'temp_home/payments.html', context)
    return redirect(request, '/')


def payment_success(request, total=0):
    if request.user.is_authenticated:
        order = Order.objects.filter(user=request.user).order_by('-id').first()
        payment_method = PaymentMethod.objects.get(id=2)
        payment = Payment(
            user = request.user,
            payment_method = payment_method,
            amount_paid = order.order_total,
            status = 'paid'
        )
        payment.save()
        
        order.payment = payment
        order.status = 'accepted'
        order.save()
        cart_items = CartItem.objects.filter(user = request.user)

        cart_items = CartItem.objects.filter(user=request.user)
        for cart_item in cart_items:
            product_price = 0
            if cart_item.product.offer:
                product_price = cart_item.product.get_offer_price()
            if cart_item.product.category.offer:
                product_price = cart_item.product.get_offer_price_by_category()
            else:
                product_price = cart_item.product.price
            print("****************", product_price, "***********************")
            orderitem = OrderItem(
                user = request.user,
                order = order,
                product = cart_item.product,
                product_price = product_price,
                quantity = cart_item.quantity,
                status = 'accepted',
            )
            orderitem.save()
            total += cart_item.sub_total()

        #reduce the stock of ordered product.
            product = Product.objects.get(id=cart_item.product.id)
            product.stock -= cart_item.quantity
            product.save()


        order = Order.objects.filter(user=request.user).order_by('-id').first()
        order_item = OrderItem.objects.filter(user=request.user)
        CartItem.objects.filter(user=request.user).delete()

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

    per_page = 5
    page_number = request.GET.get('page')
    paginator = Paginator(order_items, per_page)

    try:
        current_page = paginator.page(page_number)

    except PageNotAnInteger:
        current_page = paginator.page(1)

    except EmptyPage:
        current_page = paginator.page(paginator.num_pages)

    context  ={
        "current_page" : current_page,
    } 
    return render(request, 'temp_home/user_order_list.html', context)
    


def user_order_cancel(request, id):
    order_item = OrderItem.objects.get(id=id)
    if order_item.status == "accepted":
        order_item.status = "Cancelled"
        order_item.save()
    return redirect(user_order_list )


def user_order_detail(request, id):
    order_item = OrderItem.objects.get(id=id)
    context = {
        'order_item': order_item
    }
    return render(request, 'temp_home/order_item_details.html', context)


def order_invoice(request, id):
    order = Order.objects.get(id=id, user = request.user)
    order_items = OrderItem.objects.filter(order=order)
    print("**************************", order, "************************")
    print("**************************", order_items, "************************")

    for order_item in order_items:
        order_item.total_price = order_item.product.price * order_item.quantity

    context = {
        "order": order,
        "order_items": order_items,
    }
    return render(request, 'order_invoice.html', context)
