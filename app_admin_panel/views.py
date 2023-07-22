from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth.models import User
from app_order.models import *
from app_products.models import *
from app_authors.models import *
from django.db.models import Q

# Create your views here.
#<<<<<<<<<<<<<<<<<<<<   checks if the user is authenticated and super user  >>>>>>>>>>>>>>>>>>>>
def super_admincheck(user):
    if user.is_authenticated and user.is_superuser:
        return True
    return False


#<<<<<<<<<<<<<<<<<<<<   redirect to the admin dashboard  >>>>>>>>>>>>>>>>>>>>
def admin_dashboard(request):
    if request.user.is_authenticated and request.user.is_superuser:
       
       # filtering the delivered items from the OrderItem
      


        revenue = 0
        order_count = OrderItem.objects.count()
        # order_count = delivered_item.count()
        product_count = Product.objects.count()
        author_count = Authors.objects.count()
        category_count = Category_list.objects.count()
        user_count = User.objects.count()                                                                                             

        #order status 
        pending_count = OrderItem.objects.filter(Q(status="pending") | Q(status="Pending")).count()
        accepted_count = OrderItem.objects.filter(Q(status="accepted") | Q(status="Accepted")).count()
        shipped_count = OrderItem.objects.filter(Q(status="shipped") | Q(status="Shipped")).count()
        delivered_count = OrderItem.objects.filter(Q(status="delivered") | Q(status="Delivered")).count()
        cancelled_count = OrderItem.objects.filter(Q(status="cancelled") | Q(status="Cancelled")).count()
        refunded_count = OrderItem.objects.filter(Q(status="refunded") | Q(status="Refunded")).count()

        context = {
            'order_count' : order_count,
            'product_count' : product_count,
            'author_count' : author_count,
            'category_count' : category_count,
            'user_count' : user_count,
             #order status
            'pending_count' : pending_count,
            'accepted_count' : accepted_count,
            'shipped_count' : shipped_count,
            'delivered_count' : delivered_count,
            'cancelled_count' : cancelled_count,
            'refunded_count' : refunded_count,
           
        }
        
        return render(request, 'adminpanel/ad_dashboard.html', context)
    return render(request, 'adminpanel/admin_login.html')


#<<<<<<<<<<<<<<<<<<<<   admin login function  >>>>>>>>>>>>>>>>>>>>
def adminlogin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('pass1')

        user = authenticate(username = username, password = password)

        if user is not None and user.is_superuser:
            login(request, user)
            return redirect('admin_dashboard')
        else:
            messages.error(request, 'invalid superuser credentials')
            login(request, 'adminlogin')

    if request.user.is_authenticated and request.user.is_superuser:
        return redirect('admin_dashboard')
    return render(request, 'adminpanel/admin_login.html')


#<<<<<<<<<<<<<<<<<<<<   admin logout function  >>>>>>>>>>>>>>>>>>>>
@login_required
@user_passes_test(super_admincheck)
def admin_logout(request):
    logout(request)
    return redirect(adminlogin)


#<<<<<<<<<<<<<<<<<<<<  user details page to get all user detail   >>>>>>>>>>>>>>>>>>>>
@login_required
@user_passes_test(super_admincheck)
def user_details(request):
    user = User.objects.all()

    return render(request, 'adminpanel/user.html', {'users':user})


#<<<<<<<<<<<<<<<<<<<<  to block a user in the admin side  >>>>>>>>>>>>>>>>>>>>
@login_required
@user_passes_test(super_admincheck)
def block_user(request, id):
    user = User.objects.get(id=id)
    name = user.first_name
    user.is_active = False
    user.save()
    messages.success(request, f'User " {name} " is blocked')
    return redirect(user_details)


#<<<<<<<<<<<<<<<<<<<<  to unblock a user in the admin side  >>>>>>>>>>>>>>>>>>>>
@login_required
@user_passes_test(super_admincheck)   
def unblock_user(request, id):
    user = User.objects.get(id=id)
    name = user.first_name
    user.is_active = True
    user.save()
    messages.success(request, f'User " {name} " is unblocked')
    return redirect(user_details)



#<<<<<<<<<<<<<<<<<<<<  Sales report  >>>>>>>>>>>>>>>>>>>>

def sales_report(request):
    if not request.user.is_superuser:
        return redirect(admin_dashboard)
    
    context = {}

    if request.method == "POST":
        start_date = request.POST.get("start_date")
        end_date = request.POST.get("end_date")

        if start_date == "" :
            messages.error(request, 'start date not entered')
            return redirect(sales_report)
        if end_date == "" :
            messages.error(request, 'end date not entered')
            return redirect(sales_report)
        
        if start_date == end_date:
            date_obj = datetime.strptime(start_date, '%Y-%m-%d')
            order_items = OrderItem.objects.filter(order__created_at__date = date_obj.date())
            if order_items:
                context.update(sales = order_items, s_date = start_date, e_date = end_date)
                return render(request, 'adminpanel/sales.html')
            else:
                pass
            




def base(request):
    return render(request, 'adminpanel/base.html')