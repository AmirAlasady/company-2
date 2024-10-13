
from django.urls import path
from .views import *

urlpatterns = [

    path('ceoindex/',ceoindex,name='ceoindex'),
    path('ceo_profile/',ceo_profile,name='ceo_profile'),
    path('change/<int:pk>',change,name='change'),
    path('deltask/<int:pk>',deltask,name='deltask'),
    path('createtask/',createtask,name='createtask'),
    path('file_list/', file_list, name='file_list'),
    path('upload/', file_upload, name='file_upload'),
    path('download/<int:file_id>/', file_download, name='file_download'), 
    path('delete/<int:file_id>/', file_delete, name='file_delete'),  
    path('asignTask/',asignTask,name='asignTask'),
    path('ceo_task_asigner_deltask/<int:pk>', ceo_task_asigner_deltask, name='ceo_task_asigner_deltask'),
    path('ceo_task_asigner_change_task/<int:pk>',ceo_task_asigner_change_task,name='ceo_task_asigner_change_task'),
    path('generate_report/',generate_report,name='generate_report'),
]