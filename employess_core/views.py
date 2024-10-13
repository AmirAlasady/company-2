import os
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from .models import *
from shared.models import *
from helpers import is_employee
from root.models import Profile
from django.core.exceptions import PermissionDenied
from company import settings
# Create your views here.


def employeeindex(request):
    is_employee(request)
    todoelements=todoemployee.objects.all().filter(author=request.user)
    context={"todoelements":todoelements}
    return render(request,'employeeindex.html',context=context)

def validate_image_file(profile_photo):
    allowed_mimetypes = ['image/jpeg', 'image/png']
    return profile_photo.content_type in allowed_mimetypes and profile_photo.size <= 36700160  # 35MB limit

def employee_profile(request):
    is_employee(request)
    if request.method == "POST":
        PIC = request.FILES.get('profile_photo')
        if PIC:
            if validate_image_file(PIC):
                try:
                    user_profile = Profile.objects.get(user=request.user)
                except Profile.DoesNotExist:
                    # Profile doesn't exist, create a new one
                    user_profile = Profile.objects.create(user=request.user)
                # Update profile photo in either case
                user_profile.profile_photo = PIC
                user_profile.save()
                
    user_x =  request.user
    current_user = request.user.username

    try:
        user_profile = Profile.objects.get(user=user_x)
        profile_photo_url=user_profile.profile_photo.url
    except :
        profile_photo_url=None 
    
    context= {
        "user_x":user_x,
        "current_user":current_user,
        "profile_photo_url":profile_photo_url
    }
    return render(request, 'employee_profile.html',context)

def employee_change(request,pk):
    is_employee(request)
    thing=todoemployee.objects.get(id=pk)
    if thing.author != request.user:
        raise PermissionDenied("unauthorized access")
    if request.method == 'POST':
        updatedtask=request.POST.get('new_task')
        thing.task=updatedtask
        thing.save()
        return redirect('employeeindex')
    context={"thing":thing}
    return render(request,'employee_task_detailed.html',context=context)

def employee_deltask(request,pk):
    is_employee(request)
    thing=todoemployee.objects.get(id=pk)
    if thing.author != request.user:
        raise PermissionDenied("unauthorized access")
    if request.method == 'POST':
        if thing.done:
            thing.delete()
            return redirect('employeeindex')
        else:
            messages.warning('task is not yet done !')
            return redirect('employeeindex')
            #raise PermissionDenied("task is not yet done!")
        
    

def employee_createtask(request):
    is_employee(request)
    if request.method == 'POST':
        taskdisc=request.POST.get('taskdisc')
        todoemployee.objects.create(task=taskdisc,author=request.user).save()
        return redirect('employeeindex')

def employee_change_task_status(request,pk):
    is_employee(request)
    task=todoemployee.objects.get(id=pk)
    if task.author != request.user:
        raise PermissionDenied("unauthorized access")
    if request.method == 'POST':
        done = request.POST.get('done')  # Get the selected radio button value
        if done == 'False':
            task.done=False
        if done == 'True':
            task.done=True
        task.save()
        return redirect('employee_change',pk)
    else:
        raise PermissionDenied("unauthorized get")

#---------------
def employee_change_password(request, user_id):
    is_employee(request)
    user = get_object_or_404(User, id=user_id)
    if user == request.user:
        if request.method=='POST':
            print(user_id)
            new_pass=request.POST.get('new_pass')
            user.set_password(new_pass)
            user.save()
            messages.success(request, f"Password change for user {user.email} not yet implemented.")
            return redirect('login')
    else:
        raise PermissionDenied("error!")


def employee_change_email(request, user_id):
    is_employee(request)
    user = get_object_or_404(User, id=user_id)
    if user == request.user:
        if request.method=='POST':
            new_email=request.POST.get('new_email')
            if new_email in User.objects.all().filter(email=new_email):
                messages.warning(request, "email already exists")
                return redirect('change_email',user_id=user.id)
            user.email=new_email
            user.save()
            messages.success(request, f"email change for user {user.email} not yet implemented.")
            return redirect('employee_profile')
    else:
        raise PermissionDenied("error!")
    

def employee_change_username(request,user_id):
    is_employee(request)
    
    user = get_object_or_404(User, id=user_id)
    if user == request.user:
        if request.method=='POST':
            new_username=request.POST.get('new_username')
            user.username=new_username
            user.save()
            messages.success(request, f"username change for user {user.email} ")
            return redirect('employee_profile')
    else:
        raise PermissionDenied("error!")
    

def employee_file_list(request):
    is_employee(request)  # Ensure this is implemented to check user roles, if necessary

    # Get search parameters from GET request
    search_query = request.GET.get('search', '')

    # Filter files based on the search parameters
    files = File.objects.all().filter(owner=request.user)

    if search_query:
        files = files.filter(title__icontains=search_query)

    return render(request, 'employee_file_list.html', {
        'files': files,
        'results': files,
    })

def employee_file_upload(request):
    is_employee(request)
    if request.method == 'POST':
        title = request.POST.get('title')
        file = request.FILES.get('file')

        if file:
            # Get the original filename with extension
            filename, extension = os.path.splitext(file.name)

            # Combine the new title with the extracted extension
            if title:
                new_filename = f'{title}{extension}'
            else:
                new_filename = f'{filename}{extension}'
            
            # Create a new File object and save it with the modified filename
            new_file = File(title=new_filename, file=file, owner=request.user)
            new_file.save()
            return redirect('employee_file_list')
        else:
            # Handle form validation errors
            return render(request, 'file_upload.html', {'error': 'Please provide all required fields.'})

    return render(request, 'file_upload.html')

def employee_file_download(request, file_id):
    is_employee(request)
    file = get_object_or_404(File, id=file_id)
    if file.owner == request.user:
        # Optional: Check permissions or ownership here if needed
        response = HttpResponse(file.file, content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename="{file.title}"'
        return response
    else:
        raise PermissionDenied("error!")
    
def employee_file_delete(request, file_id):
    file = get_object_or_404(File, id=file_id)
    if file.owner == request.user:
        # Delete the file record from the database
        file.delete()
        
        # Delete the file from the file system
        file_path = os.path.join(settings.MEDIA_ROOT, file.file.name)
        if os.path.isfile(file_path):
            os.remove(file_path)
        
        return redirect('employee_file_list')
    
    else:
        raise PermissionDenied("error!")

