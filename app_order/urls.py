from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('place_order/', views.place_order, name="place_order"),
    path('payments/', views.payments, name="payments"),

    
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)