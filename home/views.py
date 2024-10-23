"""Views for home."""
from typing import Any
from django.views.generic import View, TemplateView
from django.shortcuts import render

from products.models import Category

from site_module.models import Slider
from products.models import Product
from orders.models import Order


class HomeView(TemplateView):
    """Home View."""
    template_name = 'home/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.objects.filter(parent__isnull=True)
        sliders = Slider.objects.filter(is_active=True)
        latest_products = Product.objects.all()[:8]
        if self.request.user.is_authenticated:
            user_order, _ = Order.objects.get_or_create(is_paid=False, user=self.request.user)
            context['user_order'] = user_order
            
        context['categories'] = categories
        context['sliders'] = sliders
        context['latest_products'] = latest_products

        return context


class HeaderComponentView(TemplateView):
    template_name = 'includes/header_component.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            user_order, _ = Order.objects.get_or_create(is_paid=False, user=self.request.user)
            
            context['user_order'] = user_order

        return context 
