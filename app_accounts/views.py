from django.http import HttpResponseRedirect
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control


# Create your views here.
def signup(request):
# capturing the form input values from the HTTP POST request 
    if request.method == "POST":
        firstname = request.POST.get("firstname")
        lastname = request.POST.get("lastname")
        username = request.POST.get("username")
        email = request.POST.get("email")
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')
    
        
# Form validation for signup details
        if User.objects.filter(username=username):
            messages.error(request, "username already exist!")
            return redirect('signup')
        
        if User.objects.filter(email=email):
            messages.error(request, "email already exist!")
            return redirect('signup')
        
        if not username:
            messages.error(request, "please enter the usernmae")
            return redirect('signup')
        
        if not username.isalnum():
            messages.error(request, "Username must be alpha numeric!")
            return redirect('signup')
        
        if len(username)>10:
            messages.error(request, "username must be contain lessthan 10 characters!")
            return redirect('signup')
        
        if not firstname:
            messages.error(request, "please enter your name")
            return redirect('signup')
        
        if not pass1:
            messages.error(request, "please enter a password")
            return redirect('signup')
        
        if not pass2:
            messages.error(request, "please confirm your password")
            return redirect('signup')
        
        if pass1 != pass2:
            messages.error(request, "password does not match")
            return redirect('signup')
        
        if len(pass1)<8:
            messages.error(request, "password must contain minimum 10 characters!")
            return redirect('signup')
        
        user_obj = User.objects.create( email=email, username=username )

        user_obj.set_password(pass1)
        user_obj.save()

        messages.warning(request, "An email has been sent your mail")
        

    return render(request, "accounts/signup.html")


def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        pass1 = request.POST.get('pass1')

        user_email = User.objects.filter(email = email)

        if not user_email[0].profile.is_email_varified:
            messages.warning(request, "your account is not varified!")
            return redirect('login')

        user_obj = User.objects.filter(username= username)
        if user_obj.exists():
            messages.warning(request, "Acount not found")
            return redirect('login')

        user_obj = authenticate(request, username = username, password = pass1)

        if user_obj is not None:
            login(request, user_obj)
            messages.success('logged in')
            return redirect('/')
        else:
            messages.error(request, "invalid username of password")
            return redirect('login')
    
    


    return render(request, "accounts/login.html")

def logout(request):
    return redirect(request, "app_accounts/login")


