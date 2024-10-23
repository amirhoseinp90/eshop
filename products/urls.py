from django.urls import path

from . import views


urlpatterns = [
    path('products', views.SearchProdutView.as_view(), name='search-product'),
    path('products/<slug:slug>', views.ProductDetailView.as_view(), name='product-detail'),
]