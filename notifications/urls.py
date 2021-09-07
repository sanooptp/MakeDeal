from django.contrib import admin
from django.urls import path, include
from . import views
import notifications

urlpatterns = [
    path('chat', views.index, name='index'),
    path('chat/<str:room_name>/', views.room, name='room'),
    path('delete-notification/<pk>', views.DeleteNotificationView.as_view(), name='delete-notification')
]       