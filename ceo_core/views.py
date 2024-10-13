import os
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from company import settings
from helpers import is_ceo
from root.models import Profile
from .models import *
from shared.models import *
from accounts.models import *
import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.platypus import Table, TableStyle
from datetime import datetime
from django.core.files.base import ContentFile
from io import BytesIO
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter, inch
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle
from django.core.files.base import ContentFile
from datetime import datetime
import arabic_reshaper
from bidi.algorithm import get_display
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from io import BytesIO



# Create your views here.
def ceoindex(request):

    # auth + per here...
    is_ceo(request)
    
    #business logic here...
    todoelements=todoceo.objects.all()
    context={"todoelements":todoelements}
    return render(request,'ceoindex.html',context=context)

def createtask(request):
    is_ceo(request)
    if request.method == 'POST':
        taskdisc=request.POST.get('taskdisc')
        todoceo.objects.create(task=taskdisc).save()
        return redirect('ceoindex')

def change(request,pk):
    is_ceo(request)
    thing=todoceo.objects.get(id=pk)
    if request.method == 'POST':
        updatedtask=request.POST.get('new_task')
        thing.task=updatedtask
        thing.save()
        return redirect('ceoindex')
    context={"thing":thing}
    return render(request,'task_detailed.html',context=context)

def deltask(request,pk):
    is_ceo(request)
    thing=todoceo.objects.get(id=pk)
    if request.method == 'POST':
        thing.delete()
        return redirect('ceoindex')



# profile is unique to oeach user as set internally in the user app

def validate_image_file(profile_photo):
    allowed_mimetypes = ['image/jpeg', 'image/png']
    return profile_photo.content_type in allowed_mimetypes and profile_photo.size <= 36700160  # 35MB limit


def ceo_profile(request):
    is_ceo(request)
    
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
    return render(request, 'ceo_profile.html',context)



def file_list(request):
    is_ceo(request)  # Ensure this is implemented to check user roles, if necessary

    # Get search parameters from GET request
    search_query = request.GET.get('search', '')
    user_query = request.GET.get('user', '')

    # Filter files based on the search parameters
    files = File.objects.all()

    if search_query:
        files = files.filter(title__icontains=search_query)

    if user_query:
        # Filter files based on the username associated with the owner
        matching_users = User.objects.filter(username__icontains=user_query)
        files = files.filter(owner__in=matching_users)
    reports_list = reports.objects.all()
    return render(request, 'file_list.html', {
        'files': files,
        'results': files,
        "reports_list":reports_list
    })

def file_upload(request):
    is_ceo(request)
    if request.method == 'POST':
        title = request.POST.get('title')
        file = request.FILES.get('file')

        if file:
            # Get the original filename with extension
            filename, extension = os.path.splitext(file.name)

            # Combine the new title with the extracted extension
            if title:
                # Manually set the new file name with the correct extension
                new_filename = f'{title}{extension}'
            else:
                new_filename = f'{filename}{extension}'
            
            # Assign the new filename to the file's `name` attribute
            file.name = new_filename
            #print(file.name)
            # Create a new File object and save it with the modified filename
            new_file = File(title=new_filename, file=file, owner=request.user)
            new_file.save()
            return redirect('file_list')
        else:
            # Handle form validation errors
            return render(request, 'file_upload.html', {'error': 'Please provide all required fields.'})

    return render(request, 'file_upload.html')


import zipfile
from io import BytesIO
from django.http import HttpResponse

def file_download(request, file_id):
    is_ceo(request)
    file = get_object_or_404(File, id=file_id)

    # Create a ZIP file in memory
    buffer = BytesIO()
    with zipfile.ZipFile(buffer, 'w') as zip_file:
        # Add file to the ZIP archive with the original filename
        zip_file.writestr(file.title, file.file.read())

    buffer.seek(0)
    
    # Create response
    # Ensure the downloaded ZIP file has a clean name without an extra .zip
    response = HttpResponse(buffer, content_type='application/zip')
    response['Content-Disposition'] = f'attachment; filename="{file.title}"'

    return response


def file_delete(request, file_id):
    is_ceo(request)
    file = get_object_or_404(File, id=file_id)

    # Delete the file record from the database
    file.delete()
    
    # Delete the file from the file system
    file_path = os.path.join(settings.MEDIA_ROOT, file.file.name)
    if os.path.isfile(file_path):
        os.remove(file_path)
    
    return redirect('file_list')



def asignTask(request):
    is_ceo(request)
    users = User.objects.all().filter(is_ceo=False)

    # asign a user some task 
    if request.method == 'POST':
        task_description = request.POST.get('task')
        author_id = request.POST.get('author')

        # Basic validation
        if not task_description or not author_id:
            # Handle invalid input (e.g., display error message)
            return render(request, 'create_task.html', {'error_message': 'Task and author are required'})

        try:
            author = User.objects.get(id=author_id)
        except User.DoesNotExist:
            # Handle invalid author (e.g., display error message)
            return render(request, 'asignTask.html', {'error_message': 'Invalid author'})

        new_task = todoemployee(task=task_description, author=author,by_ceo=True)
        new_task.save()
        return redirect('asignTask')  # Replace with your task list URL
    search_user = request.GET.get('search_user', '')
    if search_user:
        users_todo = todoemployee.objects.filter(author__username__icontains=search_user)
    else:
        users_todo = todoemployee.objects.all()

    context = {
        "users":users,
        "users_todo": users_todo,
        "search_user": search_user,  # Pass the search term to the template
    }
    return render(request, 'asignTask.html', context)

def ceo_task_asigner_deltask(request,pk):
    is_ceo(request)
    thing=todoemployee.objects.get(id=pk)
    if request.method == 'POST':
        thing.delete()
        return redirect('asignTask')
        


def ceo_task_asigner_change_task(request,pk):
    is_ceo(request)
    thing=todoemployee.objects.get(id=pk)
    if request.method == 'POST':
        updatedtask=request.POST.get('new_task')
        thing.task=updatedtask
        thing.save()
        return redirect('asignTask')






def generate_report(request):
    is_ceo(request)  # Ensure this function is correctly defined in your project
    data = todoemployee.objects.all()

    # Create a PDF file
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter  # Get the page size

    # Set the font and font size
    font = 'Helvetica'  # Change this to a font that supports Arabic if necessary
    arabic_font = 'Arial'  # Ensure you have a font that supports Arabic characters
    pdfmetrics.registerFont(TTFont('Arial', 'arial.ttf'))  # Register the Arabic-supporting font
    font_size = 12

    # Add the date and time
    date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    c.setFont(font, font_size)
    c.drawString(1 * inch, height - 1 * inch, 'Date: ' + date_time)  # Position date at the top

    # Define space for the table, ensuring it does not touch the date line
    margin = 0.5 * inch  # Add a margin between the date and the table
    table_y_position = height - 2 * inch - margin  # Adjust as needed to create space for the date

    # Create a table
    table_data = []
    table_data.append(['Task', 'Date Created', 'Author', 'Done', 'By CEO'])
    for task in data:
        task_name = task.task
        if any('\u0600' <= char <= '\u06FF' for char in task_name):  # Check if there's Arabic text
            reshaped_text = arabic_reshaper.reshape(task_name)  # Reshape the text for proper display
            task_name = get_display(reshaped_text)  # Make it RTL
        table_data.append([task_name, task.date_Created, task.author, task.done, task.by_ceo])

    # Create a table style
    table_style = TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.5, (0, 0, 0)),
        ('FONTNAME', (0, 0), (-1, -1), font),
        ('FONTSIZE', (0, 0), (-1, -1), font_size),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 1), (-1, -1), arabic_font),  # Use Arabic font for data rows
    ])

    # Create the table
    table = Table(table_data, style=table_style)

    # Add the table to the PDF
    table.wrapOn(c, width - 2 * inch, height - 2 * inch)  # Adjust dimensions if needed
    table.drawOn(c, 1 * inch, table_y_position)  # Draw table below the date

    # Save the PDF
    c.showPage()
    c.save()

    # Save the PDF to the model
    pdf_file = buffer.getvalue()
    buffer.close()
    reports.objects.create(title=f"Report - {date_time}", file=ContentFile(pdf_file, name=f"report_{date_time}.pdf"))

    # Return the PDF as a response
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="report_{date_time}.pdf"'
    return response

