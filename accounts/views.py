
from django.shortcuts import render,redirect
from root.models import User
from .generator.gen import generator
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from helpers import is_ceo
from django import forms
# Create your views here.


def signup(request):
    is_ceo(request)
    if request.method=="POST":
        email=request.POST['email']
        password=request.POST['password1']
        password_confirm=request.POST['password2']
        username=request.POST['username']
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        if password!=password_confirm:
            messages.warning(request,'something went wrong!')
            return render(request,'signup.html')
        try:
            if User.objects.get(username=email):
                messages.warning(request,'already a user')
                return render(request,'signup.html')
        except Exception as identifire:
            pass
        print(f'{email} | {last_name}')
        user = User.objects.create_user(
            email=email,
            username=username,
            first_name=first_name,
            last_name=last_name,
            is_ceo=False
            )
        user.set_password(password)
        user.save()
        messages.info(request,'user created')
        return redirect('signup')
    #print(request.user.is_authenticated)
    results=''
    try:
        username=request.GET.get('username','')
        if username:
            results=User.objects.all().filter(username=username)
            #print(results)
    except:
        print('no data')
    users=User.objects.all().filter(is_superuser=False,is_staff=False,is_ceo=False)
    context={"users":users,
             "results":results}
    return render(request,'signup.html',context)



def multiusercreation(request):
    is_ceo(request)
    if request.method=='POST':
        user_count=int(request.POST.get('user_count') )
        if user_count == 0:
            assert 'error'
        for i in range(user_count):
            data = generator.generate_data()
            if data['password']!=data['re_password']:
                messages.error(request, 'must be at least 1')
                return redirect('signup')
            else:
                worker_account=User.objects.create(
                    email=data['email'],
                    username=data['username'],
                    first_name=data['first_name'],
                    last_name=data['last_name'],
                    is_ceo=False
                )
            worker_account.set_password(data['password'])
            worker_account.save()
        messages.info(request,'users created secessfully')
        return redirect('signup')



def details(request, user_id):
    is_ceo(request)
    user=User.objects.get(pk=user_id)
    print(f'email {user.email} | username {user.username}')
    context={"user_wanted":user,
            "use_id":user_id,
             "user_email":user.email,
             "user_username":user.username,
             "f_name":user.first_name,
             "l_name":user.last_name,
             "status":user.is_active,
             "user_last_login":user.last_login,
             "is_ceo":user.is_ceo}
    return render(request,'details.html',context)


def change_password(request, user_id):
    is_ceo(request)
    user = get_object_or_404(User, id=user_id)
    if request.method=='POST':
        print(user_id)
        new_pass=request.POST.get('new_pass')
        user.set_password(new_pass)
        user.save()
        messages.success(request, f"Password change for user {user.email} not yet implemented.")
        return redirect('details',user_id)
    


def change_email(request, user_id):
    is_ceo(request)
    user = get_object_or_404(User, id=user_id)

    if request.method=='POST':
        new_email=request.POST.get('new_email')
        if new_email in User.objects.all().filter(email=new_email):
            messages.warning(request, "email already exists")
            return redirect('change_email',user_id=user.id)
        user.email=new_email
        user.save()
        messages.success(request, f"email change for user {user.email} not yet implemented.")
        return redirect('details',user_id)
    

def change_username(request,user_id):
    is_ceo(request)
    
    user = get_object_or_404(User, id=user_id)
    if request.method=='POST':
        new_username=request.POST.get('new_username')
        user.username=new_username
        user.save()
        messages.success(request, f"username change for user {user.email} ")
        return redirect('details',user_id)



def change_status(request,user_id):
    is_ceo(request)
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        new_status=request.POST.get('new_status')
        #print(f'type {type(new_status)} | status {new_status}')
        if new_status == 'False':
            user.is_active=False
        if new_status == 'True':

            user.is_active=True

        user.save()
        #print(f'status {user.is_active}')
        messages.success(request, f"User {user.email} status changed successfully.")
        return redirect('details',user_id)
    


def delete_user(request, user_id):
    is_ceo(request)
    user = get_object_or_404(User, id=user_id)


    if request.method == 'POST':
        user.delete()
        messages.success(request, f"User {user.email} deleted successfully.")
        return redirect('signup')


    



def ceo_change_password(request, user_id):
    is_ceo(request)
    user = get_object_or_404(User, id=user_id)
    if request.method=='POST':
        print(user_id)
        new_pass=request.POST.get('new_pass')
        user.set_password(new_pass)
        user.save()
        messages.success(request, f"Password change for user {user.email} not yet implemented.")
        return redirect('login')
    


def ceo_change_email(request, user_id):
    is_ceo(request)
    user = get_object_or_404(User, id=user_id)

    if request.method=='POST':
        new_email=request.POST.get('new_email')
        if new_email in User.objects.all().filter(email=new_email):
            messages.warning(request, "email already exists")
            return redirect('change_email',user_id=user.id)
        user.email=new_email
        user.save()
        messages.success(request, f"email change for user {user.email} not yet implemented.")
        return redirect('ceo_profile')
    

def ceo_change_username(request,user_id):
    is_ceo(request)
    
    user = get_object_or_404(User, id=user_id)
    if request.method=='POST':
        new_username=request.POST.get('new_username')
        user.username=new_username
        user.save()
        messages.success(request, f"username change for user {user.email} ")
        return redirect('ceo_profile')





