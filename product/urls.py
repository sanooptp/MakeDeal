from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import DeleteProductView, EditProductView, ProducView, ProductCreateView, MyProductView, acceptpurchase, mark_sold, mark_unsold,rejectpurchase
urlpatterns = [
    path('createproduct',ProductCreateView.as_view(), name='createproduct'),
    path('myproducts', MyProductView.as_view(), name= 'myproducts'),
    path('product/<int:id>/', ProducView.as_view(), name= 'product'),
    path('editproduct/<int:id>/', EditProductView.as_view(), name= 'editproduct'),
    path('<pk>/acceptpurchase/', acceptpurchase, name= 'acceptpurchase'),
    path('<pk>/rejectpurchase/', rejectpurchase, name= 'rejectpurchase'),
    path('<pk>/deleteproduct/', DeleteProductView.as_view(), name='deleteproduct'),
    path('<pk>/marksold/', mark_sold, name='marksold'),
    path('<pk>/mark-unsold/', mark_unsold, name='markunsold'),

    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)