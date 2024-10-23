"""Url mappings for accounts view."""
from django.urls import path
from . import views


app_name = 'accounts'
urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('account_verification/', views.AccountVerificationView.as_view(), name='account-verification'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),

    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('personal-info/', views.PersonalInfoView.as_view(), name='personal-info'),
    path('shopping-cart/', views.ShoppingCartView.as_view(), name='shopping-cart'),
    path('order/', views.OrderView.as_view(), name='orders')
]