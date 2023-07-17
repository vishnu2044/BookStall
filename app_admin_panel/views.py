from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth.models import User

# Create your views here.
#<<<<<<<<<<<<<<<<<<<<   checks if the user is authenticated and super user  >>>>>>>>>>>>>>>>>>>>
def super_admincheck(user):
    if user.is_authenticated and user.is_superuser:
        return True
    return False


#<<<<<<<<<<<<<<<<<<<<   redirect to the admin dashboard  >>>>>>>>>>>>>>>>>>>>
@login_required
@user_passes_test(super_admincheck)
def admin_dashboard(request):
    if request.user.is_authenticated and request.user.is_superuser:
        member = User.objects.all()
        return render(request, 'adminpanel/ad_dashboard.html',{'member':member})
    return render(request, 'adminpanel/admin_login.html')


#<<<<<<<<<<<<<<<<<<<<   admin login function  >>>>>>>>>>>>>>>>>>>>
def adminlogin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('pass1')

        user = authenticate(username = username, password = password)

        if user is not None and user.is_superuser:
            login(request, user)
            return redirect('admin_dashboard')
        else:
            messages.error(request, 'invalid superuser credentials')
            login(request, 'adminlogin')

    if request.user.is_authenticated and request.user.is_superuser:
        return redirect('admin_dashboard')
    return render(request, 'adminpanel/admin_login.html')


#<<<<<<<<<<<<<<<<<<<<   admin logout function  >>>>>>>>>>>>>>>>>>>>
@login_required
@user_passes_test(super_admincheck)
def admin_logout(request):
    logout(request)
    return redirect(adminlogin)


#<<<<<<<<<<<<<<<<<<<<  user details page to get all user detail   >>>>>>>>>>>>>>>>>>>>
@login_required
@user_passes_test(super_admincheck)
def user_details(request):
    user = User.objects.all()

    return render(request, 'adminpanel/user.html', {'users':user})


#<<<<<<<<<<<<<<<<<<<<  to block a user in the admin side  >>>>>>>>>>>>>>>>>>>>
@login_required
@user_passes_test(super_admincheck)
def block_user(request, id):
    user = User.objects.get(id=id)
    name = user.first_name
    user.is_active = False
    user.save()
    messages.success(request, f'User " {name} " is blocked')
    return redirect(user_details)


#<<<<<<<<<<<<<<<<<<<<  to unblock a user in the admin side  >>>>>>>>>>>>>>>>>>>>
@login_required
@user_passes_test(super_admincheck)   
def unblock_user(request, id):
    user = User.objects.get(id=id)
    name = user.first_name
    user.is_active = True
    user.save()
    messages.success(request, f'User " {name} " is unblocked')
    return redirect(user_details)




def base(request):
    return render(request, 'adminpanel/base.html')