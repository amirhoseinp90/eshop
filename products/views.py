from typing import Any
from django.shortcuts import render
from django.views.generic import TemplateView, DetailView

from .models import Product
from .forms import AddToCartForm
from orders.models import Order, OrderDetail


class SearchProdutView(TemplateView):
    template_name = 'products/search-product.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        q = self.request.GET.get('q')
        products = Product.objects.filter(title__icontains=q)

        context['products'] = products
        return context

class ProductDetailView(DetailView):
    template_name = 'products/product-detail.html'
    context_object_name = 'product'
    queryset = Product.objects.all()

    def post(self, request, *args, **kwargs):
        form = AddToCartForm(request.POST)

        if form.is_valid():
            product = form.cleaned_data['product']
            quantity = form.cleaned_data['quantity']
            user_order, _ = Order.objects.get_or_create(is_paid=False, user=self.request.user)
            
            try:
                order_detail = OrderDetail.objects.get(order=user_order,product=product,)
                order_detail.count += quantity
                order_detail.save()
            except:
                order_detail = OrderDetail.objects.create(
                    order=user_order,product=product, 
                    count=quantity
                )
            
        return render(request, self.template_name)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        has_in_cart = False
        quantity = 0

        if self.request.user.is_authenticated:
            try:
                order = Order.objects.get(user=self.request.user, is_paid=False)
                product = Product.objects.get(slug=self.request.GET.get('slug'))
                order_details = order.order_details.filter(product=product)
                if order_details.exists():
                    has_in_cart = True
                    quantity = order_details.first().quantity
            except:
                pass

        context['has_in_cart'] = has_in_cart
        context['quantity'] = quantity

        return context 




