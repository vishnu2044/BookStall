from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from app_order.models import *
from app_products.models import *
from app_authors.models import *
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta
from django.db.models import F
from django.db.models import Sum
import calendar
from django.db.models import Count
from app_admin_panel.views import *
from datetime import date


# Create your views here.
#sales calculation 
def sales_calculation(start_date, end_date):
        if start_date == end_date:
            date_obj = start_date.strftime("%Y-%m-%d")
            order_items = OrderItem.objects.filter(order__created_at__date = date_obj)
        else:
            order_items = OrderItem.objects.filter(order__created_at__gte = start_date, order__created_at__lte = end_date)

        if order_items:
            order_count = order_items.distinct('order').count()
            order_item_count = order_items.count()

            # <<<<<<<<<< payement methods >>>>>>>>>>>
            delivered_items = order_items.filter(status__iexact="delivered")
            delivered_items_count = order_items.filter(status__iexact="delivered").count()

            #total revenue
            product_price_sum = 0
            for item in delivered_items:
                product_price_sum += (item.product_price * item.quantity)
            #Through razor pay
            raz_total = 0
            raz_method = PaymentMethod.objects.get(id=2)  
            raz_orders = Order.objects.filter(payment__payment_method=raz_method)
            razorpay_items = delivered_items.filter(order__in=raz_orders)

            for item in razorpay_items:
                raz_total += (item.product_price * item.quantity)

            ## Through cod  ##
            cod_total = 0
            cod_method = PaymentMethod.objects.get(id=1)  
            cod_orders = Order.objects.filter(payment__payment_method=cod_method)  
            cod_items = delivered_items.filter(order__in=cod_orders)  

            for item in cod_items:
                cod_total += ( item.product_price * item.quantity)

            calculation  ={
                'delivered_items_count' : delivered_items_count,
                'order_item_count' : order_item_count,
                'product_price_sum' : product_price_sum,
                'order_count' : order_count,
                'raz_total' : raz_total,
                'cod_total' : cod_total,

            }
            return calculation
        


def sales_report(request):
    if not request.user.is_superuser:
        return redirect(admin_dashboard)
    
    context = {}
    s_date = None
    e_date = None
    start_date = None
    end_date = None
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
            date_obj = datetime.strftime(start_date, '%Y-%m-%d')
            order_items = OrderItem.objects.filter(order__created_at__date=date_obj.date())

            if order_items:
                context.update(sales_calculation(start_date, end_date))
                context.update(sales = order_items, s_date = start_date, e_date = end_date)
                messages.success(request, f'Here is the sales report as of {end_date}. ')

                return render(request, 'adminpanel/sales.html' ,context)
            else:
                messages.error(request, "No data found for the specific date!")

            return redirect(sales_report)
        
        order_items = OrderItem.objects.filter(order__created_at__gte=start_date, order__created_at__lte=end_date)
            
        if order_items:
            context.update(sales = order_items, s_date = start_date, e_date = end_date)
            context.update(sales_calculation(start_date, end_date))

            messages.success(request, f'Here is the sales report covering the period from {start_date} to {end_date}.')
        else:
            messages.error(request, 'No data found at the specific date!')
    

    return render(request, 'adminpanel/sales.html', context)




def today_report(request):
    context = {}
    today = date.today()
    
    date_obj = today.strftime("%Y-%m-%d")
    order_items = OrderItem.objects.filter(order__created_at__date = date_obj)

    if order_items:
        context.update(sales = order_items, s_date=today, e_date=today)
        messages.success(request, f'Here is the sales report as of {date_obj}. ')
        context.update(sales_calculation(today, today))

        return render(request, 'adminpanel/sales.html' ,context)
    else:
        messages.error(request, 'no data found.')
        return render(request, 'adminpanel/sales.html')


def week_report(request):
    context = {}
    today = date.today()
    week = today - timedelta(days=7)

    order_items = OrderItem.objects.filter(order__created_at__gte = week, order__created_at__lte = today)

    if order_items:
        context.update(sales = order_items, s_date = today, e_date = week)
        context.update(sales_calculation(week, today))
        messages.success(request, f'Here is the sales report as of last week')
        return render(request, 'adminpanel/sales.html' ,context)
    
    else:
        messages.error(request, 'no data found in the last week.')
        return render(request, 'adminpanel/sales.html')




def month_report(request):
    context = {}
    today = date.today()
    month = today - timedelta(days=30)

    order_items = OrderItem.objects.filter(order__created_at__gte = month, order__created_at__lte = today)

    if order_items:
        context.update(sales = order_items, s_date = today, e_date = month)
        context.update(sales_calculation(month, today))
        print("************************************* context : ",context, "***********************************************************")
        messages.success(request, 'Here is the sales report of last month')
        return render(request, 'adminpanel/sales.html', context)
    
    else:
        messages.error(request, 'no data found')
        return render(request, 'adminpanel/sales.html')

