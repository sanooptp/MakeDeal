from purchase.views import  PurchasedView
from django.urls import path, include
from .views import DeletePurchaseView, PurchasedView

urlpatterns = [
    path('purchased', PurchasedView.as_view(), name= 'purchased'),
    path('<pk>/deletepurchase/', DeletePurchaseView.as_view(), name='deletepurchase')
]