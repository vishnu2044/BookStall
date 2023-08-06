from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('adminlogin/', views.adminlogin, name="adminlogin"),
    path('', views.admin_dashboard, name="admin_dashboard"),
    path('admin_logout', views.admin_logout, name="admin_logout"),
    path('base', views.base, name="base"),
    path('user_details', views.user_details, name="user_details"),
    path('block_user/<int:id>/', views.block_user, name="block_user"),
    path('unblock_user/<int:id>/', views.unblock_user, name="unblock_user"),
    path('sales_report', views.sales_report, name="sales_report"),
    path('today_report', views.today_report, name="today_report"),
    

    
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
