from django.shortcuts import redirect, render
from django.contrib import messages
from app_category.models import Category
import uuid
from django.shortcuts import get_object_or_404, redirect

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
            Category.objects.get(category_name = name )
        except:
            Category.objects.create(category_name = name, 
                                    slug = slug , 
                                    category_description = descripiton)
            messages.success(request,f'Category "{name}" succesfully added')
        else:
            messages.error(request, f'category "{name} is already exist !')
            return redirect(add_category)
        
    if not request.user.is_authenticated and not request.user.is_superuser:
        return redirect('admin_dashboard')
    categories = Category.objects.all()
    context = {
        'categories' : categories,
    }
    return render(request, 'adminpanel/categories.html', context)


def edit_catgory(request, id):
    pass

# def delete_category(request, id):
#     category = Category.objects.get(id=id)
#     name = category.category_name
#     category.is_available = False
#     category.save()
#     messages.success(request, f'category "{name}" is deleted.')
#     return redirect(add_category)


def delete_category(request, id):
    category_uuid = uuid.UUID(id)
    category = get_object_or_404(Category, uuid=category_uuid)
    name = category.category_name
    category.is_available = False
    category.save()
    messages.success(request, f'Category "{name}" is deleted.')
    return redirect('add_category')
