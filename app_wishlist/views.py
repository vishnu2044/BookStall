from django.shortcuts import render, redirect
from .models import Wishlist
from app_products.models import Product
from django.contrib import messages
from app_home.views import *


# Create your views here.
def wishlist_view(request):
    user = request.user
    wishlist_items = Wishlist.objects.filter(user = user)

    context = {
        'wishlist_items' : wishlist_items,
    }

    return render(request, 'temp_home/wishlist.html', context)



def add_to_wishlist(request, id):
    product = Product.objects.get(id=id)
    user = request.user

    if Wishlist.objects.filter(user=user, product=product).exists():
        messages.info(request, f'{product.product_name} already in the wishlist!')
        referring_url = request.META.get('HTTP_REFERER')

        if referring_url:
            return redirect(referring_url)
        else:
            return redirect(wishlist_view)
    else:
        wishlist_item = Wishlist.objects.create(user=request.user, product=product)
        wishlist_item.save()
        messages.success(request, "Added successfully!")

    # Get the referring URL
        referring_url = request.META.get('HTTP_REFERER')

        if referring_url:
            return redirect(referring_url)
        else:
            return redirect(wishlist_view)


def remove_from_wishlist(request, id):
    product = Product.objects.get(id=id)
    user = request.user
    wishlist_item = Wishlist.objects.get(product = product)
    if wishlist_item :
        wishlist_item.delete()
        messages.success(request, f'{product.product_name} romved from Wishlist')

        # Get the referring URL
        referring_url = request.META.get('HTTP_REFERER')
        if referring_url:
            return redirect(referring_url)
        else:
            return redirect(wishlist_view)

    else:
        messages.warning(request, f"{product.product_name} not present in wishlist")

                # Get the referring URL
        referring_url = request.META.get('HTTP_REFERER')
        if referring_url:
            return redirect(referring_url)
        else:
            return redirect(wishlist_view)

