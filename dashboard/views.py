from decimal import Context

from django.views.generic import detail
from dashboard.models import UserDetails
from django.db import models
from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from .forms import UserDetailsForm, UserEditForm, UserRegisterForm
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.core.mail import EmailMessage, send_mail
from .tokens import account_activation_token
from django.conf import settings
from product.models import Product


class DashboardView(LoginRequiredMixin, generic.ListView):
    template_name = 'dashboard/dashboard.html'  
    model = Product
    context_object_name = 'products'

class SignUpView(generic.CreateView):
    form_class = UserRegisterForm 
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

    def get(self, request):
        form = self.form_class()
        profile_form = UserDetailsForm()
        return render(request, 'registration/signup.html', {'userform': form, 'profile_form': profile_form})
    
    def post(self, request):
        if request.method == 'POST':
            form = self.form_class(request.POST)
            profile_form = UserDetailsForm(request.POST)
            
            if form.is_valid() and profile_form.is_valid():
                email = form.cleaned_data.get('email')
                if User.objects.filter(email=email).exists():
                     return HttpResponse('Email exists, Please login')
                else:
                    user = form.save(commit=False)
                    user.is_active = False
                    user.save()

                    # Saving user profile
                    profile = profile_form.save(commit=False)
                    profile.user = user
                    profile.save()
                    messages.success(request,  'Your account has been successfully created')

                    
                    # Sending email verification
                    current_site = get_current_site(request)
                    mail_subject = 'Activate your blog account.'
                    message = render_to_string('registration/acc_active_email.html', {
                        'user': user,
                        'domain': current_site.domain,
                        'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                        'token':account_activation_token.make_token(user),
                    })
                    to_email = form.cleaned_data.get('email')
                    # email = EmailMessage(
                    #             mail_subject, message, to=[to_email]
                    # )
                    # email.send()
                    email_from = settings.EMAIL_HOST_USER
                    send_mail( mail_subject, message, email_from, [to_email] )
                    return HttpResponse('Please confirm your email address to complete the registration')
        else:
            form = self.form_class()
            profile_form = UserDetailsForm()
        return render(request, 'registration/signup.html', {'userform': form, 'profile_form': profile_form})


class IndexView(generic.TemplateView):
    template_name = 'dashboard/index.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')
        return super(IndexView, self).get(request, *args, **kwargs)
    
def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')

class ProfileView(LoginRequiredMixin, generic.ListView):
    template_name= 'dashboard/profile.html'
    
    def get(self, request):
        userdetails = UserDetails.objects.get(user= request.user)
        context = {'userdetails': userdetails}
        return render (request, self.template_name, context)

class ProfileEditView(LoginRequiredMixin, generic.CreateView):
    template_name= 'dashboard/editprofile.html'
    form_class = UserEditForm
    
    def get(self, request):
        userform = User 
        details = self.form_class()
        context = {'userform': userform, 'details': details}
        return render(request, self.template_name, context )


