from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
# ----------------------Pass reset-----------------------------
from django.contrib.auth import update_session_auth_hash
# ----------------------Pass reset-----------------------------
# ----------------------send mail------------------------------
import uuid
from .models import *
from django.core.mail import send_mail
from django.http import JsonResponse
from django.conf import settings


# ----------------------send mail------------------------------
# Create your views here.

# --------------------------------------forget section---------
def Forget_pass(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('pass')
        if email:
            user = User.objects.get(email=email)
            user.set_password(password)
            user.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'User password changed successfully.')
            return redirect('signin')
        else:
            messages.error(request, 'email not matched.')
    return render(request, 'accounts/forget_password.html')


# --------------------------------------forget section----------------------------

# --------------------------------------Registration section----------------------------
def sign_up(request):
    if request.method == 'POST':
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password1 = request.POST['password1']

        if len(password) == 0 and len(password1) == 0:
            messages.warning(request, "Input Password !!!")
        else:
            if password == password1:
                if User.objects.filter(username=username).exists():
                    messages.warning(request, "Username Already Taken !!!")
                elif User.objects.filter(email=email).exists():
                    messages.warning(request, "email Already Taken !!!")
                else:
                    user = User.objects.create_user(first_name=firstname, last_name=lastname, username=username,
                                                    email=email, password=password)
                    user.set_password(password)
                    user.save()
                    auth_token = str(uuid.uuid4())

                    pro_obj = Profile.objects.create(user=user, auth_token=auth_token)
                    pro_obj.save()
                    send_mail_registration(email, auth_token)
                    return render(request, 'accounts/success.html')
            else:
                messages.warning(request, "Password not matched !!!")

    return render(request, 'accounts/signup.html')


# --------------------------------------Registration section----------------------------

# --------------------------------------Sigin section----------------------------
def sign_in(r):
    if r.user.is_authenticated:
        return redirect('home')

    if r.method == 'POST':
        username = r.POST.get('name')
        password = r.POST.get('pass')
        user = auth.authenticate(username=username, password=password)
        if user:
            prof = Profile.objects.get(user=user)
            if prof.is_verified is True:
                auth.login(r, user)
                messages.warning(r, "User Logged in.")
                return redirect('home')
            else:
                messages.warning(r, "Verify your account.")
                return redirect('signup')

        else:
            messages.warning(r, "User Not Found.")
            return redirect('signup')
    return render(r, 'accounts/signin.html')


# --------------------------------------signin section----------------------------


# --------------------------------------Signout section----------------------------
def signout(r):
    auth.logout(r)
    return redirect('signin')


# --------------------------------------Signout section----------------------------

def success(r):
    return render(r, 'success.html')


def fail(r):
    return render(r, 'fail.html')


def send_mail_registration(email, token):
    subject = "Account Verification link"
    message = f'hi click the link for verify http://127.0.0.1:8000/accounts/verify/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)


def verify(request, auth_token):
    profile_obj = Profile.objects.filter(auth_token=auth_token).first()
    profile_obj.is_verified = True
    profile_obj.save()
    messages.success(request, 'OWWO,your mail is verified')
    return redirect('signin')
