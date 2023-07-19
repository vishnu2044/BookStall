from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name="home"),
    path('about/', views.about, name="about"),
    path('shop/', views.shop, name="shop"),
    path('base', views.base, name="base"),
    path('product_details/<int:id>/', views.product_details, name="product_details"),
    
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
