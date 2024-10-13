"""
URL configuration for company project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import *
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('root.urls')),
    path('ceo_core/',include('ceo_core.urls')),     # root linker application ceo 1
    path('accounts/',include('accounts.urls')),     # functions as 
    path('employess_core/',include('employess_core.urls')),
    path('chat/',include('chat.urls')),
    path('ai/',include('ai.urls'))
]
urlpatterns += static(settings.MEDIA_URL, view=protected_media_view) 