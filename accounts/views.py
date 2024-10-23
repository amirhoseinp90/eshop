"""Views for accounts."""
from django.shortcuts import redirect
from django.views.generic import View, TemplateView
from django.shortcuts import render
from django.http.response import HttpResponse
from django.contrib.auth import get_user_model, login, logout

from .mixins import SendEamilMixin
from accounts.models import AuthenticateCode
from orders.models import Order, OrderDetail
from .forms import (
    RegisterForm,
    AccountVerificationForm,
    LoginForm,
    PersonalInfoForm
)  


User = get_user_model()


class RegisterView(View, SendEamilMixin):
    """View for user registration."""
    form_class = RegisterForm
    template_name = 'accounts/register.html'
    email_template = 'emails/email_verification.html'

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('home:home')
        
        form = self.form_class()

        return render(request, self.template_name, {'form': form})
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save()

            self.request.session['_auth_verify_user_pk'] = user.pk


            self.auth_code = AuthenticateCode.objects.create(
                user=user,
                email=user.email,
                code = str(random.randint(10000000,99999999))
            )
            
            self.send_email('فعال سازی حساب کاربری', form.cleaned_data.get('email'))

            return redirect('accounts:account-verification')
        
        return render(request, self.template_name, {'form':form})
    
    def get_email_context(self):
        context = super().get_email_context()
        context['auth_code'] = self.auth_code.code

        return context

    
class AccountVerificationView(View):
    """Verify user account with an authentication code."""
    template_name = 'accounts/account_verification.html'
    form_class = AccountVerificationForm
    
    def get(self, request, *args, **kwargs):
        if not '_auth_verify_user_pk' in request.session or request.user.is_authenticated:
            return redirect('home:home')
        
        form = self.form_class()
        
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        if not '_auth_verify_user_pk' in request.session:
            return HttpResponse({'msg': 'cookies must be enabaled'} ,safe=False, status=400)

        if self.request.user.is_authenticated:
            return HttpResponse({'msg': 'please first log out'}, safe=False, status=400)
        
        form = self.form_class(request.POST)
        
        if form.is_valid():
            user_pk = request.session.get('_auth_verify_user_pk')
            user = User.objects.get(pk=user_pk)
            
            auth_code = user.authenticatecode
            if form.cleaned_data['code'] == auth_code.code and not auth_code.is_expired:
                user.is_email_verified=True
                user.save()
                login(request, user)
                auth_code.delete()
                # your account has been successful verified
                return redirect('/')
            
            form.add_error('code', 'invalid code')
        
        return render(request, self.template_name, {'form': form})


class LoginView(View):
    template_name = 'accounts/login.html'
    form_class = LoginForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()

        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.cleaned_data.get('user')
            login(request, user)
            return redirect('/')


        return render(request, self.template_name, {'form':form})


class LogoutView(View):
    def post(self, request, *args, **kwargs):
        # TODO set message indicating that the user has been sucessfully loged out
        logout(request)
        return redirect('/')


class ProfileView(View):
    template_name = 'accounts/profile/profile.html'
    
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})

class PersonalInfoView(View):
    template_name = 'accounts/profile/personal-info.html'
    form_class = PersonalInfoForm

    def get(self, request, *args, **kwargs):
        form = self.form_class(instance=request.user)

        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            form = self.form_class(instance=request.user)
            
        return render(request, self.template_name, {'form':form})


class ShoppingCartView(TemplateView):
    template_name = 'accounts/profile/shopping-cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            user_order, _ = Order.objects.get_or_create(is_paid=False, user=self.request.user)
            
            context['user_order'] = user_order
            print('test' * 20)

        return context 

class OrderView(TemplateView):
    template_name = 'accounts/profile/order.html'


    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     if self.request.user.is_authenticated:
    #         user_order, _ = Order.objects.get_or_create(is_paid=False, user=self.request.user)
            
    #         context['user_order'] = user_order
    #         print('test' * 20)

    #     return context 