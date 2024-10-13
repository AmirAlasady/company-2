from django.urls import path

from . import views


urlpatterns = [
    path('users/', views.user_list, name='user_list'),
    path('start/<int:user_id>/', views.start_chat, name='start_chat'),
    path('dms/<str:room_id>/', views.chat_room, name='chat_room'),
    path('send_file/<int:user_id>/', views.send_file, name='send_file'),
    path('video/', views.videosetup, name='videosetup'),
    path('video/call/', views.video, name='video'),
    path('video/call/join', views.joinvideo, name='joinvideo'),
    path('notifications/',views.notifications,name='notifications'),
    path('notificationsdelete/<int:notification_id>/', views.notificationsdelete, name='notificationsdelete'),
]

