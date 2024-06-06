from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.views.generic import FormView
from .forms import UserRegistrationForm
from django.contrib.auth import login,logout
from django.contrib.auth.views import LoginView,LogoutView
from django.contrib import messages
from accounts.forms import DepositForm
from django.contrib.auth.mixins import LoginRequiredMixin

# email import 
from  django.core.mail import EmailMessage,EmailMultiAlternatives
from django.template.loader import render_to_string
# Create your views here.

def send__email(user,subject,template):
    message = render_to_string(template,{'user': user })
    send_email =EmailMultiAlternatives(subject,"",to =[user.email])
    send_email.attach_alternative(message,"text/html")
    send_email.send()

def send_transaction_email(user,amount,subject,template):
    message = render_to_string(template,{'user': user,'amount':amount })
    send_email =EmailMultiAlternatives(subject,"",to =[user.email])
    send_email.attach_alternative(message,"text/html")
    send_email.send()

class UserRegistrationView(FormView):
    template_name = 'accounts/user_registration.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        messages.success(self.request, 'account create Successfully')
        send__email(user,"Create account","accounts/create_account_email.html")
        return super().form_valid(form)
    
class UserLoginView(LoginView):
    template_name = 'accounts/user_login.html'
    def get_success_url(self):
        return reverse_lazy('home')
    
    def form_valid(self,form):
        messages.success(self.request,"Login successfully")
        return super().form_valid(form)
    


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('home') 
    
    def dispatch(self, request, *args, **kwargs):
        if request.method == 'GET':
            if request.user.is_authenticated:
                logout(self.request)
            return redirect(self.next_page)
        else:
            return super().dispatch(request, *args, **kwargs)
        

class DepositView(LoginRequiredMixin,FormView):
    template_name = 'accounts/deposit.html'
    form_class = DepositForm
    success_url = reverse_lazy('home')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['account'] = self.request.user.account
        return kwargs

    def form_valid(self, form):
        account = self.request.user.account
        balance =form.cleaned_data['balance']
        account.balance += balance
        messages.success(self.request,'your deposit was successfully checked your email')
        send_transaction_email(self.request.user,balance,"deposit",'accounts/depo_email.html')
        account.save()
        return super().form_valid(form)
    
    
