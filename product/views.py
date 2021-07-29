from product.models import Product
from typing import Generic
from django import forms
from django.db import models
from django.shortcuts import render
from django.urls.base import is_valid_path
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .forms import CreateProductForm, EditProductForm
from django.contrib import messages
from django.shortcuts import redirect


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
                messages.success(request,  'Product created')
                return redirect('dashboard')
            else:
                messages.success(request,  ' Invalid form   ')
                return render(request, self.template_name, {'form': form})


class MyProductView(LoginRequiredMixin,generic.ListView):
    template_name = 'product/myproducts.html'
    context_object_name = 'products'
    def get_queryset(self):
        return Product.objects.filter(user=self.request.user)

class ProducView(generic.ListView):
    template_name = 'product/product.html'
    context_object_name = 'products'

    # def get_queryset(self,request, id):
    #     return Product.objects.filter(id= id)


    def get (self, request, id):
        product = Product.objects.get(id = id)
        context= {'product': product}
        return render(request, self.template_name, context )

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
                messages.success(request, 'Profile details updated.')
                return redirect('myproducts')
        return render(request, self.template_name, {'form': form})

