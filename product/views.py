from django.http.response import HttpResponse
from dashboard.models import UserDetails
from purchase.models import Purchase
from purchase.forms import BuyForm, PurchaseStatusForm
from django.views.generic.base import TemplateView
from product.models import Product
from notifications.models import BroadcastNotification
from typing import Generic
from django import forms
from django.db import models
from django.shortcuts import render
from django.urls.base import is_valid_path, reverse
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .forms import CreateProductForm, EditProductForm
from django.contrib import messages
from django.shortcuts import redirect,get_object_or_404
from django.template.loader import render_to_string
from django.core.mail import EmailMessage, send_mail
from django.conf import settings
from django.contrib.auth.models import User
from twilio.rest import Client
from asgiref.sync import async_to_sync  
import channels.layers
from datetime import datetime  



class ProductCreateView(LoginRequiredMixin, generic.FormView):
    template_name = 'product/createproduct.html'
    form_class = CreateProductForm
    success_url = reverse_lazy('dashboard')
    login_url = '/accounts/login/'

    def post(self, request):
        if request.method == 'POST':
            form = self.form_class(request.POST, request.FILES)
            if form.is_valid():
                fm = form.save(commit= False)
                fm.user = request.user
                fm.save()
                messages.success(request,'Product created')
                return redirect('dashboard')
            else:
                messages.success(request,  ' Invalid form   ')
                return render(request, self.template_name, {'form': form})


class MyProductView(LoginRequiredMixin,generic.ListView):
    template_name = 'product/myproducts.html'
    context_object_name = 'products'
    def get_queryset(self):
        return Product.objects.filter(user=self.request.user)


class ProducView(generic.CreateView):
    template_name = 'product/product.html'
    context_object_name = 'products'

    def get (self, request, id):
        # import pdb;
        # pdb.set_trace() 
        product = Product.objects.get(id = id)
        purchase = ''
        buyform = BuyForm
        seller_product = Purchase.objects.filter(product = product, seller = request.user) #checking for myproducts as seller

        if Purchase.objects.filter(product = product, buyer = request.user):    # checking for purchases as buyer
            if Purchase.objects.filter(product = product, buyer = request.user):
                purchase = Purchase.objects.get(product = product, buyer = request.user)
            context= {'product': product, 'purchase': purchase, 'seller_product': seller_product}
        else:
            context= {'product': product, 'buyform': buyform, 'seller_product': seller_product}
        return render(request, self.template_name, context )
    
    def post(self, request, id):
        if request.method == 'POST':
            buyer = request.user
            product = Product.objects.get(id= id)
            seller = product.user
            seller_email = seller.email
            buyform = BuyForm(request.POST)
            price = buyform['buyer_price'].value()
            if buyform.is_valid():
                fm = buyform.save(commit=False)
                fm.seller = seller
                fm.buyer = buyer
                fm.status = False
                fm.product = product
                fm.save()

                #notification
                channel_layer = channels.layers.get_channel_layer()
                async_to_sync(channel_layer.group_send)(    
                    'notification_%s' % seller.username,
                    {
                        'type' : 'send_notification',
                        'message' : f'Purchase request from {buyer.username} for {product.name}',
                    }
                )
                notification = BroadcastNotification.objects.create(message= f'Purchase request from {buyer.username} for {product.name}', sent= True, to= seller )
                notification.save()

                # sending mail
                # mail_subject = 'Product purchase notification.'
                # message = render_to_string('product/emailnotification.html', {
                #     'buyer': request.user,
                #     'product': product.name,
                #     'price' : price,
                #     'seller': seller    
                # })
                # email_from = settings.EMAIL_HOST_USER
                # send_mail( mail_subject, message, email_from, [seller_email] )

                # twilio send sms
                # message_to_broadcast = ("Have you played the incredible TwilioQuest ")
                # client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
                # message = client.messages.create(
                # body=f' Product purchase notification \n Hi {seller} \n User {request.user} wants to buy your product {product.name} for the price Rs{price}.',
                # from_=settings.TWILIO_NUMBER,
                # to=f'+919656073331')

                messages.success(request, 'Purchase request submitted')
                return redirect (self.request.path_info)
            else:
                return render(request, self.template_name, {'buyform': buyform})



class EditProductView(LoginRequiredMixin,generic.CreateView):
    template_name = 'product/editproduct.html'
    form_class = EditProductForm

    def get(self, request, id):
        form = self.form_class
        if request.user.is_authenticated:
            product = Product.objects.get(id = id)
            initial_data = {
                'name' : product.name,
                'description' : product.description,
                'location' : product.location,
                'category' : product.category,
                'image1' : product.image1,
                'image2' : product.image2,
                'image3' : product.image3,
                'image4' : product.image4,
                'price': product.price,
                'time_to_publish' : product.time_to_publish
            }
            form = self.form_class(initial = initial_data)
            context= {'form': form, 'product': product}
            return render(request, self.template_name, context)
        else:
            return redirect('login')
    
    def post(self, request, id):
        if request.method == 'POST':
            # import pdb
            # pdb.set_trace()
            product = Product.objects.get(id=id)
            form = self.form_class(request.POST, request.FILES, instance= product)
            if form.is_valid():
                fs = form.save(commit = False)
                fs.user =request.user
                form.save()
                messages.success(request, 'Product details updated.')
                return redirect('myproducts')
        return render(request, self.template_name, {'form': form})


def acceptpurchase(request, pk):
    purchase = get_object_or_404(Purchase, pk=pk)
    purchase.status = True
    purchase.save(update_fields=['status'])
    seller_email = purchase.seller.email
    print(seller_email)
    mail_subject = 'Product purchase notification.'
    message = render_to_string('product/sellconfirm_mail.html', {
        'buyer': request.user,
        'product': purchase.product.name,
        'price' : purchase.buyer_price,
        'seller': purchase.seller
    })
    email_from = settings.EMAIL_HOST_USER
    send_mail( mail_subject, message, email_from, [seller_email] )
    return redirect('myproducts')


def rejectpurchase(request, pk):
    purchase = get_object_or_404(Purchase, pk=pk)
    purchase.status = False
    purchase.save(update_fields=['status'])
    return redirect('myproducts')
    

class DeleteProductView(generic.DeleteView):
    model = Product
    success_url = reverse_lazy('myproducts')
    template_name = 'product/deleteconfirm.html'


def mark_sold(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.is_sold = True
    product.save(update_fields=['is_sold'])
    return redirect ('myproducts')


def mark_unsold(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.is_sold = False
    product.save(update_fields=['is_sold'])
    return redirect ('myproducts')