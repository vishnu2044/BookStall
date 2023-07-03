from django.shortcuts import redirect, render
from django.contrib import messages
from app_category.models import Category_list
from django.shortcuts import get_object_or_404, redirect
from django.core.exceptions import ObjectDoesNotExist


# Create your views here.

#<<<<<<<<<<   categories  >>>>>>>>>>

def categories_list(request):
    return render(request, 'adminpanel/categories.html')

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
    messages.success(request, f'Category "{name}" is unlisted.')
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



