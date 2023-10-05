from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User


# Create your views here.


def Forget_pass(request):
    return render(request, 'accounts/forget_password.html')


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
                    messages.success(request, "User Created !!!")
                    return redirect('signin')
            else:
                messages.warning(request, "Password not matched !!!")

    return render(request, 'accounts/signup.html')


def sign_in(request):
    return render(request, 'accounts/signin.html')
