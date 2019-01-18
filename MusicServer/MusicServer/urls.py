"""MusicServer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path
from Server import views as server_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', server_view.register, name='register'),
    path('login/', server_view.login, name='login'),
    path('index/<str:username>/', server_view.index, name='index'),
    path('register/', server_view.register, name='register'),
    path('logout/', server_view.logout, name='logout'),
    path('getAttr/', server_view.getAttr, name='getAttr'),
    path('index/<str:username>/userinfo/', server_view.userinfo, name='userinfo'),
    path('index/<str:username>/detail/<str:table>/<str:key>/', server_view.detail, name='detail'),
    path('index/<str:username>/playlist/', server_view.playlist, name='playlist'),
    path('index/<str:username>/playlist/createlist/', server_view.createlist, name='createlist'),
    path('alterPlayList/', server_view.alterPlayList),
    path('getCreateList/', server_view.getCreateList),
    path('alterSong/', server_view.alterSong),
]
