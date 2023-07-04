from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('login/', views.handle_login, name="handle_login"),
    path('signup/', views.signup, name="signup"),
    path('otp_login/', views.otp_login, name="otp_login"),
    path('user_logout/', views.user_logout, name="user_logout"),
    path('block_user/<int:id>/', views.block_user, name="block_user"),
    path('unblock_user/<int:id>/', views.unblock_user, name="unblock_user"),
    
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
