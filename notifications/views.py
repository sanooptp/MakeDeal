# chat/views.py
from notifications.models import BroadcastNotification
from django.shortcuts import render
from django.views import generic
from notifications.models import BroadcastNotification

def index(request):
    return render(request, 'notifications/index.html', {})

def room(request, room_name):
    return render(request, 'notifications/room.html', {
        'room_name': room_name
    })

class DeleteNotificationView(generic.DeleteView):
    model= BroadcastNotification
    success_url =('/')
    
