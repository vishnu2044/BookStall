from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin_authors/', views.admin_authors, name = 'admin_authors'),
    path('add_author/', views.add_author, name = 'add_author'),
    path('add_author_page/', views.add_author_page, name = 'add_author_page'),
    path('edit_author/<int:id>/', views.edit_author, name = 'edit_author'),
 
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


