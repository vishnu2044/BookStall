import random
from django.http import HttpResponseRedirect
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages ,auth
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.conf import settings
from django.core.mail import send_mail
from .models import Profile, UserAddress
from app_admin_panel.views import *
from django.db import IntegrityError
# from django.contrib.auth.hashers import check_password
import logging

logger = logging.getLogger(__name__)


# Create your views here.
    #<<<<<<<<<<<<<<<<<<<< --------------------- >>>>>>>>>>>>>>>>>>>>
    #<<<<<<<<<<<<<<<<<<<< --------------------- >>>>>>>>>>>>>>>>>>>>
    #<<<<<<<<<<<<<<<<<<<<  user authentication  >>>>>>>>>>>>>>>>>>>>
    #<<<<<<<<<<<<<<<<<<<< --------------------- >>>>>>>>>>>>>>>>>>>>
    #<<<<<<<<<<<<<<<<<<<< --------------------- >>>>>>>>>>>>>>>>>>>>

#<<<<<<<<<<<<<<<<<<<<  To create a new acount for a new user  >>>>>>>>>>>>>>>>>>>>
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
            
            
            myuser = User.objects.create_user(username = username, email = email)
            myuser.set_password(pass1)
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
            return render(request, "accounts/signup.html", {'otp':True, 'usr':myuser})
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
                return render(request, 'accounts/signup.html', {'otp':True, 'usr':user})

    return render(request, "accounts/signup.html", {'otp':False})


#<<<<<<<<<<<<<<<<<<<<  To login a user for authorisation  >>>>>>>>>>>>>>>>>>>>
def handle_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        pass1 = request.POST.get('pass1')

        if not User.objects.filter(username = username):
            messages.error(request, "Invalid User name")
            return redirect(handle_login)
        
        if username is None :
            messages.warning("please enter username")
            return redirect(handle_login)
        
        if pass1 is None:
            messages.warning(request, "Please enter password")

        user = authenticate(request, username = username, password = pass1)

        if user is not None:
            login(request, user)
            messages.success(request,'logged in')
            return redirect('/')
        else:
            messages.error(request, "invalid password")
            return redirect(handle_login)
        
    if request.user.is_authenticated:
        return redirect('/')
    return render(request, "accounts/login.html")



#<<<<<<<<<<<<<<<<<<<<  To login a user using otp  >>>>>>>>>>>>>>>>>>>>
def otp_login(request):

    if request.method == "POST":
        get_otp = request.POST.get('otp')
        if not get_otp:
            email = request.POST.get('email')
            try: 
                user = User.objects.get(email=email)
            except:
                messages.error(request, f"This is not a valid email id ")
                return redirect(otp_login)
            
            if user is not None:
                otp = int(random.randint(1000,9999))
                profile = Profile(user = user, otp = otp)
                profile.save()
                mess=f"Hello {user.username},\nYour OTP to login to your acount for BookStall is {otp}\nThanks"
                send_mail(
                    "Welcome to BookStall Varify your email for login.",
                    mess,
                    settings.EMAIL_HOST_USER,
                    [user.email],
                    fail_silently=False
                )
                return render(request, 'accounts/otp_login.html', {"otp":True, "usr":user})
        
        else:
            get_email = request.POST.get('email')
            user = User.objects.get(email=get_email)
            profile = Profile.objects.get(user=user)
            if get_otp == Profile.objects.filter(user=user).last().otp:
                login(request, user)
                messages.success(request, f"Successfully logined {user.email}")
                Profile.objects.filter(user=user).delete()
                return redirect('/')
            else:
                messages.warning(request, f"You entered a wrong OTP")
                return render(request, 'accounts/otp_login.html', {"otp": True, "usr":user})
    
    if request.user.is_authenticated:
        return redirect('/')
    return render(request, 'accounts/otp_login.html' )
    
    



#<<<<<<<<<<<<<<<<<<<<  To log out a user from the site  >>>>>>>>>>>>>>>>>>>>
@login_required(login_url='handle_login')
def user_logout(request):
    logout(request)
    return HttpResponseRedirect("/")





    
    #<<<<<<<<<<<<<<<<<<<< --------------------- >>>>>>>>>>>>>>>>>>>>
    #<<<<<<<<<<<<<<<<<<<< --------------------- >>>>>>>>>>>>>>>>>>>>
    #<<<<<<<<<<<<<<<<<<<< user profile settings >>>>>>>>>>>>>>>>>>>>
    #<<<<<<<<<<<<<<<<<<<< --------------------- >>>>>>>>>>>>>>>>>>>>
    #<<<<<<<<<<<<<<<<<<<< --------------------- >>>>>>>>>>>>>>>>>>>>
     
     
def user_profile(request):
    if request.user.is_authenticated:

        address = UserAddress.objects.filter(user=request.user)
        user = request.user

        context = {
            'user' : user,
            'addresses': address,
        }

        return render(request, 'temp_home/user_profile.html', context)
    return redirect('home')

def change_password(request):

    if request.method == "POST":
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        user = request.user
        if not user.is_authenticated:
            messages.error(request, 'please login first !')
            return redirect(request, 'handle_login')

        if not user.check_password(old_password):
            messages.error(request, 'please enter the correct password !')
            return redirect(change_password)

        if new_password != confirm_password:
            messages.error(request, "Password mismatch")
            return redirect(request, change_password)

        user.set_password(new_password)
        user.save()
        auth.login(request, user)
        messages.success(request, "password changed successfully !")
        return redirect(user_profile)

    else:
        return render(request, 'temp_home/change_password.html')


def edit_user_profile(request):
    if request.method == "POST":
        username = request.POST.get("username")
        fname = request.POST.get("firstname")
        lname = request.POST.get("lastname")
        print(username,"   ", fname,"     ", lname)


        edited_user = request.user
        edited_user.first_name = fname
        edited_user.username = username
        edited_user.last_name = lname
        edited_user.save()
        
        messages.success(request, 'profile updated successfully.')
        return redirect(user_profile)
    return render(request, 'temp_home/edit_profile.html')


# def add_user_address_profile(request):
#     if request.method == "POST":
#         name = request.POST.get("name")
#         ph_no = request.POST.get("number")
#         house = request.POST.get("house")
#         landmark = request.POST.get("landmark")
#         district = request.POST.get("district")
#         city = request.POST.get("city")
#         state = request.POST.get("state")
#         country = request.POST.get("country")
#         pincode = request.POST.get("pincode")
        
#         UserAddress.objects.create(
#             fullname = name,
#             contact_number = ph_no,    
#             user = request.user,
#             house_name = house,
#             landmark = landmark,
#             city = city,
#             district = district,
#             state = state,
#             country = country,
#             pincode = pincode,
#         ).save()
#         return redirect(user_profile)


def edit_user_address(request, id):
    if request.method == "POST":
        name = request.POST.get("name")
        ph_no = request.POST.get("number")
        house = request.POST.get("house")
        landmark = request.POST.get("landmark")
        district = request.POST.get("district")
        city = request.POST.get("city")
        state = request.POST.get("state")
        country = request.POST.get("country")
        pincode = request.POST.get("pincode")
        
        UserAddress.objects.filter(id=id).update(
            fullname = name,
            contact_number = ph_no,    
            user = request.user,
            house_name = house,
            landmark = landmark,
            city = city,
            district = district,
            state = state,
            country = country,
            pincode = pincode,
        )
        messages.success(request, "address updated.")
        return redirect(user_profile)
        
    address = UserAddress.objects.get(id=id)
    context = {
        "address": address,
    }
    return render(request, 'temp_home/edit_address.html', context)

def delete_user_address(request, id):
    address = UserAddress.objects.get(id=id)
    address.delete()
    messages.success(request, "address deleted successfully.")
    return redirect(user_profile)
