"""Warsztat URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from conference_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('all_rooms/', views.show_room),
    path('room/new/', views.AddRoom.as_view(), name='add_room'),
    path('adduser/', views.add_user, name='add_user'),
    path('all_rooms/modify_room/<int:room_id>/', views.ModifyRoom.as_view(), name='modify_room'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('all_rooms/del_room/<int:id>/', views.DelRoom.as_view(), name='delete_room'),
    path('all_rooms/reserv_room/<int:room_id>/', views.RoomReservation.as_view()),
    path('all_rooms_reservations/', views.show_room_reservations),
]
