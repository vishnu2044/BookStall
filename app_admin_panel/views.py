from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User

# Create your views here.
def admin_dashboard(request):
    if request.user.is_authenticated and request.user.is_superuser:
        member = User.objects.all()
        return render(request, 'adminpanel/ad_dashboard.html',{'member':member})
    return render(request, 'adminpanel/admin_login.html')



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

def admin_logout(request):
    logout(request)
    return redirect(adminlogin)

def base(request):
    return render(request, 'adminpanel/base.html')

def user(request):
    return render(request, 'adminpanel/user.html')