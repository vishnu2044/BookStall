from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('category/', views.categories_list, name = 'categories_list'),
    path('addcategory/', views.add_category, name = 'add_category'),
    path('unlistcategory/<int:id>/', views.unlist_category, name = 'unlist_category'),
    path('listcategory/<int:id>/', views.list_category, name = 'list_category'),
    path('editcategory/<int:id>/', views.edit_catgory, name='edit_catgory'),
    path('admin_products/', views.admin_products, name='admin_products'),
    path('add_product_page/', views.add_product_page, name='add_product_page'),
    path('add_product/', views.add_product, name='add_product'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)




