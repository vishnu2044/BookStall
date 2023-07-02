from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('category', views.categories_list, name = 'categories_list'),
    path('addcategory/', views.add_category, name = 'add_category'),
    path('deletecategory/<int:id>/', views.delete_category, name = 'delete_category'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)




