from django import forms

from products.models import Product


class AddToCartForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, max_value=5)
    product_slug = forms.IntegerField()

    
    def clean(self):
        cleaned_data = super().clean()
        product_slug = cleaned_data.get('product_slug')

        if product_slug:
            try:
                product = Product.objects.get(slug=product_slug)
            except:
                raise forms.ValidationError('مشکلی در اطلاعات وارد شده وجود دارد.')

            cleaned_data['product'] = product

        return cleaned_data

