from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('login/', views.handle_login, name="handle_login"),
    path('signup/', views.signup, name="signup"),
    path('otp_login/', views.otp_login, name="otp_login"),
    path('logout/', views.logout, name="logout"),
    
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
