from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import ProductCreateView
urlpatterns = [
    path('createproduct',ProductCreateView.as_view(), name='createproduct'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)