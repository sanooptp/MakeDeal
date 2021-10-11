from notifications.models import BroadcastNotification
def notifications(request):
    allnotifications = BroadcastNotification.objects.all()
    count = BroadcastNotification.objects.count()
    return {'notifications': allnotifications, 'count':count}