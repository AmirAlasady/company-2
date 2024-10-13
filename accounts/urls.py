from django.urls import include, path
from .views import *
urlpatterns = [
    # overwriting the user creaation djoser urls to are cutom endpoint
    path('auth/signup/',signup,name='signup'),
    path('auth/multiusercreation/',multiusercreation,name='multiusercreation'),
    path('auth/change_password/<int:user_id>/', change_password, name='change_password'),
    path('auth/change_email/<int:user_id>/', change_email, name='change_email'),
    path('auth/change_username/<int:user_id>/',change_username,name='change_username'),
    path('auth/change_status/<int:user_id>/',change_status,name='change_status'),
    path('auth/delete_user/<int:user_id>/', delete_user, name='delete_user'),
    path('auth/ceo_change_password/<int:user_id>/', ceo_change_password, name='ceo_change_password'),
    path('auth/ceo_change_email/<int:user_id>/', ceo_change_email, name='ceo_change_email'),
    path('auth/ceo_change_username/<int:user_id>/',ceo_change_username,name='ceo_change_username'),
    path('auth/details/<int:user_id>/',details,name='details'),
    #path('auth/search/', search_view, name='search_view'),
]