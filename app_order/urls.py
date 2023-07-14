from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('place_order/', views.place_order, name="place_order"),
    path('payments/', views.payments, name="payments"),
    path('user_order_list/', views.user_order_list, name="user_order_list"),
    path('user_order_cancel/<int:id>/', views.user_order_cancel, name='user_order_cancel'),

    
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)