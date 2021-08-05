from decimal import Context
from purchase.models import Purchase
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
from django.db.models import Q


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
        # import pdb
        # pdb.set_trace()
        if request.method == 'POST':
            form = self.form_class(request.POST)
            profile_form = UserDetailsForm(request.POST, request.FILES)
            
            if form.is_valid():
                if profile_form.is_valid():
                    email = form.cleaned_data.get('email')
                    # if User.objects.filter(email=email).exists():
                    #      return HttpResponse('Email exists, Please login')
                    # else:
                    user = form.save(commit=False)
                    user.is_active = False
                    user.save()

                    # Saving user profile
                    profile = profile_form.save(commit=False)
                    profile.user = user
                    profile.save()
                    messages.success(request,  'Your account has been successfully created')

                    # Saving user profile
                    
                    # Sending email verification
                    current_site = get_current_site(request)
                    mail_subject = 'Activate your account.'
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
        # count = Purchase.objects.filter(buyer = request.user).count()
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
    form_class = UserDetailsForm
    
    def get(self, request):
        getdetails = UserDetails.objects.get(user = request.user)
        userform = UserEditForm(instance= request.user)
        detailsform = self.form_class( instance = getdetails)
        context = {'userform': userform, 'detailsform': detailsform}
        return render(request, self.template_name, context)

    def post(self, request):
        # import pdb
        # pdb.set_trace()
        getdetails = UserDetails.objects.get(user = request.user)
        if request.method == 'POST':
            details_form = self.form_class(request.POST, request.FILES, instance = getdetails)
            userform = UserEditForm(request.POST, request.FILES, instance= request.user)
            if userform.is_valid():
                user = userform.save()
                user.save()

            if details_form.is_valid():
                details = details_form.save()
                details.save()
                messages.success(request, 'Profile details updated.')
                return redirect('profile')
        else:
            userform = self.form_class(instance = request.user)
            details_form = self.form_class(instance = getdetails)
            
        context = {'detailsform': details_form, 'userform': userform}
        return render(request, self.template_name, context)


# Search

class SearchResultsView(generic.ListView):
    model = Product
    template_name = 'dashboard/search_results.html'   

    def get_queryset(self): # new
        query = self.request.GET.get('search')
        object_list = Product.objects.filter(
            Q(name__icontains=query) | Q(location__icontains=query)
        )
        return object_list
    
class ShowProfileView(generic.ListView):
    template_name= 'dashboard/showprofile.html'
    
    def get(self, request,pk):
        userprofile = User.objects.get(pk=pk)
        userdetails = UserDetails.objects.get(user= userprofile)
        context = {'userdetails': userdetails, 'userprofile': userprofile}
        return render (request, self.template_name, context)