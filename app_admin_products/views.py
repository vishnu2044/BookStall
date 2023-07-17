from django.shortcuts import redirect, render
from django.contrib import messages
from app_category.models import Category_list
from django.shortcuts import get_object_or_404, redirect
from django.core.exceptions import ObjectDoesNotExist
from app_products.models import *
from django.contrib.auth.decorators import login_required, user_passes_test
from app_admin_panel.views import super_admincheck


# Create your views here.
#<<<<<<<<<<<<<<<<<<<<<<<<<  to display categories list in admin side  >>>>>>>>>>>>>>>>>>>>>>>>>
@login_required
@user_passes_test(super_admincheck)
def categories_list(request):
    categories = Category_list.objects.all()
    context = {
        'categories' : categories,
    }
    return render(request, 'adminpanel/categories.html', context)


#<<<<<<<<<<<<<<<<<<<<<<<<<  add new  category to the category list   >>>>>>>>>>>>>>>>>>>>>>>>>
@login_required
@user_passes_test(super_admincheck)
def add_category(request):
    if request.method == "POST":
        name = request.POST.get('name')
        slug = request.POST.get('slug')
        descripiton = request.POST.get('description')
        check = [name, slug]
        is_available = request.POST.get('is_available', False)
        if is_available:
            is_available = True
        else:
            is_available = False
        for values in check:
            if values == '':
                messages.info(request, 'please enter both category name and slug !')
                return redirect(add_category)
            else:
                pass
        try:
            Category_list.objects.get(category_name = name )
        except:
            Category_list.objects.create(
                                    category_name = name, 
                                    slug = slug , 
                                    category_description = descripiton
                                    )
            messages.success(request,f'Category "{name}" succesfully added')
        else:
            messages.error(request, f'category "{name} is already exist !')
            return redirect(add_category)
        
    if not request.user.is_authenticated and not request.user.is_superuser:
        return redirect('admin_dashboard')
    categories = Category_list.objects.all()
    context = {
        'categories' : categories,
    }
    return render(request, 'adminpanel/categories.html', context)


#<<<<<<<<<<<<<<<<<<<<<<<<<  Edit the excisting category items    >>>>>>>>>>>>>>>>>>>>>>>>>
@login_required
@user_passes_test(super_admincheck)
def edit_catgory(request, id):
    if request.method == "POST":
        name = request.POST.get('name')
        slug = request.POST.get('slug')
        description = request.POST.get('description')


        category = Category_list.objects.filter(id=id).update(
                    category_name = name,
                    slug = slug,
                    category_description = description
        )
        messages.success(request, f'{name} updated successfully')
        return redirect('categories_list')

    try:
        category = Category_list.objects.get(id=id)
    except Category_list.DoesNotExist:
        messages.error(request, 'Category does not exist.')
        return redirect(categories_list)

    context = {
        "category": category
    }
    return render(request, 'adminpanel/edit_category.html', context)


def unlist_category(request, id):
    try:
        category = Category_list.objects.get(id=id)
    except ObjectDoesNotExist:
        messages.error(request, 'Category does not exist.')
        return redirect(add_category)

    name = category.category_name
    category.is_available = False
    category.save()
    messages.warning(request, f'Category "{name}" is unlisted.')
    return redirect(add_category)

def list_category(request, id):
    try:
        category = Category_list.objects.get(id=id)
    except ObjectDoesNotExist:
        messages.error(request, 'Category does not exist.')
        return redirect(add_category)

    name = category.category_name
    category.is_available = True
    category.save()
    messages.success(request, f'Category "{name}" is listed.')
    return redirect(add_category)


#<<<<<<<<<<<<<<<<<<<<<<<<<  to display all prodcuts in the admin side    >>>>>>>>>>>>>>>>>>>>>>>>>
@login_required
@user_passes_test(super_admincheck)
def admin_products(request):
    products = Product.objects.all()
     
    context = {
        "products" : products,
    }
    return render(request, 'adminpanel/products_list.html', context)


def add_product_page(request):
    return render(request, 'adminpanel/add_product.html')
 

def add_product(request):
    if request.method == "POST":
        image = ''
        try:
            image = request.FILES["image"]
        except:
            if image == '':
                messages.info(request, "Image field cant't be empty !")
                return redirect(add_product)
            
        # sec_image = ''
        # try:
        #     sec_image = request.FILES['sec_image']
        # except:
        #     if sec_image =="":
        #         messages.error(request, "secondary image cant be empty!")
        #         return redirect(add_product)
            
        # prod = Product.objects.all()
        # product_instance = Product.objects.get(id=prod)
        # ProductImage.objects.create(
        #     product = product_instance,
        #     image = sec_image
        # ).save()
        
        name = request.POST.get("name")
        slug = request.POST.get("slug")
        price = request.POST.get("price")
        stock = request.POST.get("stock")
        category = request.POST.get("category")
        author = request.POST.get("author")
        description = request.POST.get("description")

        try:
            Product.objects.get(product_name = name)
        except:
            check = [name, slug, price, stock, description]
            for values in check:
                if values == "" :
                    messages.info(request, "some fields are empty !")
                    return redirect(add_product)
                else:
                    pass
                author_instance = Authors.objects.get(id=author)
                category_instance = Category_list.objects.get(id=category)
                
                Product.objects.create(
                        product_name = name,
                        slug = slug,
                        product_description = description,
                        price = price,
                        stock = stock,
                        images = image,
                        category = category_instance,
                        author = author_instance
                ).save()
                messages.success(request,f'Book : {name} added successfully')
                return redirect(admin_products)
            
    authors = Authors.objects.all()
    categories = Category_list.objects.all()

    context = {
            'categories' : categories,
            'authors' : authors,
    }
    return render(request, 'adminpanel/add_product.html', context)
 

def admin_search_prodcuts(request):
    if request.method == "GET":
        query = request.GET.get("query")
        if query:
            detail = Product.objects.filter(product_name=query)
            detail = Product.objects.filter(slug=query)
            return render(request, 'adminpanel/searchproduct.html', {"details" : detail})
        else:
            return render(request, 'admin_panel/search.html', {})


#<<<<<<<<<<<<<<<<<<<<<<<<<  Edit the excisting product details    >>>>>>>>>>>>>>>>>>>>>>>>>
@login_required
@user_passes_test(super_admincheck)
def edit_product(request, id):
    if request.method == 'POST':
        image = ''
        try:
            image = request.FILES["image"]
            print(image)
            product = Product.objects.filter(id=id).first()
            product.images = image
            product.save()
        except:
            print("HI")
        
        sec_image = ''
        try:
            sec_image = request.FILES['sec_image']
            prod = Product.objects.all()
            product_instance = Product.objects.get(id=prod)
            ProductImage.objects.create(
                product = product_instance,
                image = sec_image
            ).save()
        except:
            print("Hai")
            


        name = request.POST.get("name")
        slug = request.POST.get("slug")
        price = request.POST.get("price")
        stock = request.POST.get("stock")
        category = request.POST.get("category")
        author = request.POST.get("author")
        description = request.POST.get("description")

        if name == "":
            messages.error(request, "Product name can't be null!")
            return redirect(edit_product)
        
        author_instance = Authors.objects.get(id=author)
        categoriy_instance = Category_list.objects.get(id=category)

        product = Product.objects.filter(id=id).update(
                    product_name = name,
                    slug = slug,
                    product_description = description,
                    price = price,
                    stock = stock,
                    author = author_instance,
                    category = categoriy_instance,
            )
        messages.success(request, f'{name} updated successfully!')
        return redirect(admin_products)
    
    product = Product.objects.get(id=id)
    categories = Category_list.objects.all()
    authors = Authors.objects.all()
    context = {
        "product": product,
        "categories" : categories,
        "authors" : authors,
    }
    return render(request, 'adminpanel/edit_product.html', context)



#<<<<<<<<<<<<<<<<<<<<<<<<<  unlist the excisting prodcut details    >>>>>>>>>>>>>>>>>>>>>>>>>
@login_required
@user_passes_test(super_admincheck)
def unlist_product(request, id):
    try:
        product = Product.objects.get(id=id)
    except ObjectDoesNotExist:
        messages.error(request, 'Product does not exist.')
        return redirect(add_category)

    name = product.product_name
    product.is_available = False
    product.save()
    messages.warning(request, f'Product "{name}" is unlisted.')
    return redirect(admin_products)


#<<<<<<<<<<<<<<<<<<<<<<<<<  list the excisting prodcut details    >>>>>>>>>>>>>>>>>>>>>>>>>
@login_required
@user_passes_test(super_admincheck)
def list_product(request, id):
    try:
        product = Product.objects.get(id=id)
    except ObjectDoesNotExist:
        messages.error(request, 'Product does not exist.')
        return redirect(add_category)

    name = product.product_name
    product.is_available = True
    product.save()
    messages.warning(request, f'Product "{name}" is listed.')
    return redirect(admin_products)