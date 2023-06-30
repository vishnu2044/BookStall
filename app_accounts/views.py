import random
from django.http import HttpResponseRedirect
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.conf import settings
from django.core.mail import send_mail
from .models import Profile

# Create your views here.
def signup(request):
# capturing the form input values from the HTTP POST request 
    if request.method == "POST":
        get_otp = request.POST.get('otp')
        if not get_otp:   
            username = request.POST.get("username")  
            firstname = request.POST.get("firstname")
            lastname = request.POST.get("lastname")
            email = request.POST.get("email")
            pass1 = request.POST.get('pass1')       
            pass2 = request.POST.get('pass2')
            phone_no = request.POST.get('phno')
        
    # Form validation for signup details      
            if not username.strip():
                messages.error(request, "please enter the usernmae")
                return redirect('signup')
     
            if User.objects.filter(username = username).exists():
                messages.error(request, "usrename is already exists!")
                return redirect('signup')
     
            if not firstname.strip():
                messages.error(request, "please enter the firstname")
                return redirect('signup')
     
            if len(username)>10:
                messages.error(request, "username must be contain lessthan 10 characters!")
                return redirect('signup')
            
            if not firstname.strip():
                messages.error(request, "please enter your name")
                return redirect('signup')
            
            if User.objects.filter(email=email).exists():
                messages.error(request, "Email is already taken")
                return redirect('signup')

            if Profile.objects.filter(mobile = phone_no).exists():
                messages.error(request, "mobile number is alrady taken")
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
            
            myuser = User.objects.create_user(username = username, email = email, password = pass1)
            myuser.first_name = firstname
            myuser.last_name = lastname
            myuser.is_active = False
            myuser.save()
            otp = int(random.randint(1000,9999))
            profile = Profile(user = myuser, mobile = phone_no, otp = otp)
            profile.save()
            mess = f'hello\t{myuser.username},\nYour OTP to varify your accountfor BookStall is {otp}\nThanks!'
            send_mail(
                "Welcome to BookStall varify your Email.",
                mess,
                settings.EMAIL_HOST_USER,
                [myuser.email],
                fail_silently = False
                )
            return render(request, "accounts/signup.html", {'otp':True, 'user':myuser})
        else:
            get_email = request.POST.get('email')
            user = User.objects.get(email = get_email)
            if get_otp == Profile.objects.filter(user=user).last().otp:
                user.is_active = True
                user.save()
                messages.success(request, f'Account is created for {user.email}')
                Profile.objects.filter(user=user).delete()
                return redirect(handle_login)
            else:
                messages.warning(request, f'You entered a wrong OTP')
                return render(request, 'accounts/signup.html', {'otp':True, 'user':user})
    

        
    return render(request, "accounts/signup.html", {'otp':False})


def handle_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        pass1 = request.POST.get('pass1')

        user_obj = User.objects.filter(username= username)
        if user_obj.exists():
            messages.warning(request, "Acount not found")
            return redirect('handle_login')

        user = authenticate(request, username = username, password = pass1)

        if user is not None:
            login(request, user)
            messages.success('logged in')
            return redirect('/')
        else:
            messages.error(request, "invalid username of password")
            return redirect('handle_login')
        

    return render(request, "accounts/login.html")


from django.contrib.auth import authenticate, login

def otp_login(request):
    if request.method == "POST":
        get_otp = request.POST.get('otp')
        if not get_otp:
            email = request.POST.get('email')
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                messages.error(request, f'This is not a valid email id!')
                return redirect('otp_login')
            
            if user is not None:
                otp = int(random.randint(1000, 9999))
                profile = Profile(user=user, otp=otp)
                profile.save()
                mess = f'Hello\t{user.username},\nYour OTP to login your account for BookStall is {otp}\nThank you'
                send_mail(
                    "Welcome to BookStall, verify your Email for login",
                    mess,
                    settings.EMAIL_HOST_USER,
                    [user.email],
                    fail_silently=False
                )
                return render(request, 'accounts/otp_login.html', {'otp': True, 'user': user})
        
        else:
            get_email = request.POST.get('email')
            try:
                user = User.objects.get(email=get_email)
            except User.DoesNotExist:
                messages.error(request, f'This is not a valid email id!')
                return redirect('otp_login')

            if get_otp == Profile.objects.filter(user=user).last().otp:
                user = authenticate(request, username=user.username, password=user.password)
                if user is not None:
                    login(request, user)  # Fix: Pass the 'user' object to the login() function
                    messages.success(request, f'Successfully logged in {user.email}')
                    Profile.objects.filter(user=user).delete()
                    return redirect('/')
            else:
                messages.warning(request, f'You entered a wrong OTP')
                return render(request, 'accounts/otp_login.html', {'otp': True, 'user': user})

    return render(request, 'accounts/otp_login.html')



def logout(request):
    return HttpResponseRedirect(request, "/")

