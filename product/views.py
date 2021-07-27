from typing import Generic
from django import forms
from django.shortcuts import render
from django.urls.base import is_valid_path
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .forms import CreateProductForm
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
                fm = form.save()
                fm.save()
                messages.success(request,  'Product created')
                return redirect('dashboard')
            else:
                messages.success(request,  ' Invalid form   ')
                return render(request, self.template_name, {'form': form})

