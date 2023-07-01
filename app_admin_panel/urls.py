from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('adminlogin', views.adminlogin, name="adminlogin"),
    path('', views.admin_dashboard, name="admin_dashboard"),
    path('admin_logout', views.admin_logout, name="admin_logout"),
    path('base', views.base, name="base"),
    path('/user', views.user, name="user"),
    

    
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
