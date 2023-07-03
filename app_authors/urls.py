from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin_authors', views.admin_authors, name = 'admin_authors'),
    path('add_author', views.add_author, name = 'add_author'),
 
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


