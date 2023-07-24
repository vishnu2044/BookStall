from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('shop/', views.shop, name="shop"),
    path('product_details/<int:id>/', views.product_details, name="product_details"),
    path('product_search', views.product_search, name="product_search"),
    
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
