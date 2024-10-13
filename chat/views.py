import os
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import PrivateRoom
from root.models import User


from django.http import HttpResponse
from shared.models import File
from django.core.exceptions import PermissionDenied
# --------------
# real time communication

from django.db.models import Q

@login_required(redirect_field_name='login')
def user_list(request):
    search_query = request.GET.get('search', '')  # Get the search query from the GET parameters
    if search_query:
        # Filter users based on the search query
        users = User.objects.filter(
            Q(username__icontains=search_query) & ~Q(id=request.user.id)
        )
    else:
        # If no search query, return all users except the current one
        users = User.objects.exclude(id=request.user.id).filter(is_superuser=False)

    return render(request, "user_list.html", {"users": users, "search_query": search_query})

@login_required(redirect_field_name='login')
def start_chat(request, user_id):
    # Ensure the user exists
    other_user = get_object_or_404(User, id=user_id)
    
    # Ensure user1 is the current user and user2 is the other user
    user1, user2 = sorted([request.user, other_user], key=lambda u: u.id)
    
    # Retrieve or create a private room
    room_id = f"dm_{user1.id}_{user2.id}"
    room, created = PrivateRoom.objects.get_or_create(
        room_id=room_id,
        defaults={'name': f"{user1} and {user2}", 'user1': user1, 'user2': user2}
    )
    
    # Check if the current user is a participant
    if request.user not in [room.user1, room.user2]:
        return HttpResponseForbidden("You are not authorized to access this room.")

    return redirect('chat_room', room_id=room.room_id)

@login_required(redirect_field_name='login')
def chat_room(request, room_id):
    # Ensure the room exists and that the user is part of it
    room = get_object_or_404(PrivateRoom, room_id=room_id)
    if request.user not in [room.user1, room.user2]:
        return HttpResponseForbidden("You are not authorized to access this room.")

    return render(request, "chat_room.html", {"room_id": room_id})




# --------------
# files sedning


@login_required(redirect_field_name='login')
def send_file(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        raise PermissionDenied("User not found!")

    if request.method == 'POST':
        title = request.POST.get('title')
        file = request.FILES.get('file')

        if file:
            # Get the original filename with extension
            filename, extension = os.path.splitext(file.name)

            if title:
                # If the title does not already end with the extension, append it
                if not title.endswith(extension):
                    title += extension
                new_filename = title
            else:
                new_filename = filename + extension
            
            # Assign the new filename to the file's `name` attribute
            file.name = new_filename

            # Save the file
            new_file = File(title=new_filename, file=file, owner=user, sent_by=request.user)
            new_file.save()

            return redirect('user_list')

    return HttpResponse("Invalid request", status=400)




# video call 
@login_required(redirect_field_name='login')
def videosetup(request):
    return render(request,'videoset.html')

@login_required(redirect_field_name='login')
def video(request):
    return render(request,'videocall.html',{"name":request.user.username})

@login_required(redirect_field_name='login')
def joinvideo(request):
    if request.method == 'POST':
        meeting_url = request.POST.get('meeting_url')
        if meeting_url:
            return redirect(f"/chat/video/call/?{meeting_url.split('?')[1]}")
    return render(request, 'joinvideo.html', {"name": request.user.username})


#def notifications(request):
#    return render(request,'notifications.html')


from django.shortcuts import render
from django.http import JsonResponse
from .models import Notification


@login_required(redirect_field_name='login')
def notifications(request):
    notifications = Notification.objects.filter(recipient=request.user)
    return render(request, 'notifications.html', {'notifications': notifications})


def notificationsdelete(request, notification_id):
    try:
        notification = Notification.objects.get(id=notification_id)
        notification.delete()
        return redirect('notifications')
    except Notification.DoesNotExist:
        return redirect('notifications')


