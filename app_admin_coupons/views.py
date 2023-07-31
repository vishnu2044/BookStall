from django.shortcuts import render
from app_offer.models import Coupon

# Create your views here.
def coupons_list(request):
    coupons = Coupon.objects.all()
    context = {
        'coupons': coupons,
    }
    return render(request, 'adminpanel/coupon_list.html', context)


def add_coupon(request):
    return render(request, 'adminpanel/add_coupon.html')