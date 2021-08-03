from purchase.forms import BuyForm
from product.models import Product
from purchase.models import Purchase
from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import BuyForm
from django.shortcuts import redirect
from django.urls import reverse_lazy




class PurchasedView(LoginRequiredMixin, generic.ListView):
    template_name = 'purchase/purchased.html'
    context_object_name = 'purchase'
    def get_queryset(self):
        return Purchase.objects.filter(buyer = self.request.user)

        
class DeletePurchaseView(generic.DeleteView):
    model = Purchase
    success_url = reverse_lazy('purchased')
    template_name = 'purchase/deleteconfirm.html'