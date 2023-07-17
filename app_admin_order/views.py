from django.shortcuts import render, redirect
from app_order.models import Order, OrderItem
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from app_admin_panel.views import super_admincheck


# Create your views here.
#<<<<<<<<<<<<<<<<<<<<  To display order list in the admin side  >>>>>>>>>>>>>>>>>>>>
@login_required
@user_passes_test(super_admincheck)
def admin_order_list(request):
    order_items = OrderItem.objects.all()
    context = {
        "order_items" : order_items
    }
    return render(request, 'adminpanel/order_list.html', context)


#<<<<<<<<<<<<<<<<<<<<  To update order order status in the admin side  >>>>>>>>>>>>>>>>>>>>
@login_required
@user_passes_test(super_admincheck)
def update_order_status(request, id):
    try:
        order_item = OrderItem.objects.get(id=id)
        if request.method == "POST":
            status = request.POST["status"]
            order_item.status = status
            order_item.save()

            current_user = order_item.user
            subject = f'{order_item} {order_item.status}'
            mess = f"Hello\t{current_user.first_name}.\nYour {order_item} has been {order_item.status}, Track your order in our website.\nThank You!"
            send_mail(
                    subject,
                    mess,
                    settings.EMAIL_HOST_USER,
                    [current_user.email],
                    fail_silently= False
                )
            messages.success(request, "status updates successfully!")
            return redirect(order_details, id )

    except OrderItem.DoesNotExist:
        messages.error(request, "oops something wrong!")
        
    context = {"id":id}
    return render(order_details, context )



def order_details(request, id):
    order_item = OrderItem.objects.get(id=id)
    context = {
        "order_item" : order_item,
        "id" : id
    }
    return render(request, 'adminpanel/order_details.html', context)



