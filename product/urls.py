from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import EditProductView, ProducView, ProductCreateView, MyProductView
urlpatterns = [
    path('createproduct',ProductCreateView.as_view(), name='createproduct'),
    path('myproducts', MyProductView.as_view(), name= 'myproducts'),
    path('product/<int:id>/', ProducView.as_view(), name= 'product'),
    path('editproduct/<int:id>/', EditProductView.as_view(), name= 'editproduct')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)