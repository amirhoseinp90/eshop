from django.contrib import admin
from django.forms import BaseInlineFormSet

from . import models


class ProductImagesInlineFormset(BaseInlineFormSet):
    model = models.ProductImages
    fields = ['image']

class ProductInline(admin.StackedInline):
    model = models.ProductImages
    formset = ProductImagesInlineFormset
    extra = 1


@admin.register(models.SmartPhone)
class SmartPhoneAdmin(admin.ModelAdmin):
    inlines = [ProductInline]


admin.site.register(models.Category)
admin.site.register(models.Color)
