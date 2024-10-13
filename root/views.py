from django.shortcuts import render,redirect
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.contrib.auth import authenticate
from django.contrib.auth import logout as hlogout
from django.contrib.auth import login as auth_login
from .models import *


# Create your views here.
def login(request):
    if request.user.is_authenticated:
        messages.warning(request,'you are logged in already')
        if request.user.is_ceo:
            return redirect('ceoindex')
        else:
            return redirect('employeeindex')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(username=email, password=password)

        if user is not None:
            auth_login(request, user)
            messages.success(request, 'Logged in successfully!')

            # main system router :>>:====>>--
            #print(user.is_active)
            if user.is_ceo:
                return redirect('ceoindex')
            else:
                return redirect('employeeindex')


        else:
            messages.error(request, 'Invalid credentials')

    return render(request, 'login.html')

def logout(request):
    if not request.user.is_authenticated:
        return redirect("login")
    hlogout(request)
    messages.success(request,'logged out')
    return redirect('login')



