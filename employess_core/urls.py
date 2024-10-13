
from django.urls import path
from .views import *
urlpatterns = [
    path('employeeindex/',employeeindex,name='employeeindex'),
    path('employee_profile/',employee_profile,name='employee_profile'),
    path('employee_change/<int:pk>',employee_change,name='employee_change'),
    path('employee_deltask/<int:pk>',employee_deltask,name='employee_deltask'),
    path('employee_createtask/',employee_createtask,name='employee_createtask'),
    path('employee_change_password/<int:user_id>/', employee_change_password, name='employee_change_password'),
    path('employee_change_email/<int:user_id>/', employee_change_email, name='employee_change_email'),
    path('employee_change_username/<int:user_id>/',employee_change_username,name='employee_change_username'),
    path('employee_file_list/', employee_file_list, name='employee_file_list'),
    path('employee_upload/', employee_file_upload, name='employee_file_upload'),
    path('employee_download/<int:file_id>/', employee_file_download, name='employee_file_download'), 
    path('employee_delete/<int:file_id>/', employee_file_delete, name='employee_file_delete'),  
    path('employee_change_task_status/<int:pk>',employee_change_task_status,name='employee_change_task_status'),
    
]