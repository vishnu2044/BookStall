from django.shortcuts import render
from .models import Wishlist
from app_products.models import Product
from django.contrib import messages


# Create your views here.
def wishlist_view(request):
    user = request.user
    wishlist_items = Wishlist.objects.filter(user = user)

    context = {
        'wishlist_items' : wishlist_items,
    }

    return render(request, 'temp_home/wishlist.html', context)

def add_to_wishlist(request, product_id):
    product = Product.objects.get(id=product_id)
    user = request.user

    if Wishlist.objects.filter(user = user, product = product).exists():
        messages.info(request, f'{product.product_name} already in the wishlist!')
    else:
        wishlist_item = Wishlist.objects.create(
            user = request.user,
            product = product,
        )
        wishlist_item.save()
        messges.error(request, "added successfully!")
