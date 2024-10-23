from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from polymorphic.models import PolymorphicModel

from .enums import (
    Capacity,
    RefreshRate,
    ScreenTechnology,
    CameraNumber,
    OS
)

# class Color:
#     title = models.CharField(max_length=50)
#     hex_code = models.CharField(max_length=10)

class Category(models.Model):
    title = models.CharField(max_length=255)
    title_fa = models.CharField(max_length=255)
    slug = models.SlugField(allow_unicode=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='sub_categories', null=True, blank=True)

    def __str__(self):
        return f'{self.title}'


class ProductImages(models.Model):
    product = models.ForeignKey("Product", on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/images/')


class Product(PolymorphicModel):
    title = models.CharField(max_length=255)
    slug = models.SlugField(allow_unicode=True, null=False, blank=False, db_index=True)
    description = models.TextField()
    price = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', editable=False)
    image = models.ImageField(upload_to='products/images')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def image_galleries(self):
        images = [self.image]
        for image in self.images.all():
            images.append(image)
        return images
    

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        update_fields = kwargs.get('update_fields')
        if update_fields is not None and 'title' in update_fields:
            kwargs['update_fields'] = {'slug'}.union(update_fields)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('product-detail', args=[self.slug])


class Color(models.Model):
    title = models.CharField(max_length=255)
    title_fa = models.CharField(max_length=255)
    hex_code = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.title} : {self.hex_code}'


class SmartPhone(Product):
    weight = models.CharField(max_length=255)
    dimensions = models.CharField(max_length=255)
    sim_cart_number = models.CharField(max_length=255)
    cpu = models.CharField(max_length=255)
    cpu_frequency = models.CharField(max_length=255)
    gpu = models.CharField(max_length=255)
    internal_space = models.CharField(choices=Capacity, max_length=255)
    ram = models.CharField(choices=Capacity, max_length=255)
    refresh_rate = models.CharField(choices=RefreshRate ,max_length=255)
    screen_technology = models.CharField(choices=ScreenTechnology, max_length=255)
    radio = models.BooleanField()
    number_of_back_camera = models.CharField(choices=CameraNumber, max_length=255)
    os = models.CharField(choices=OS, max_length=255)

    _attributes = [
        'weight', 'dimensions', 'sim_cart_number', 'cpu', 'cpu_frequency', 'gpu', 'internal_space', 'ram'
        'refresh_rate', 'screen_technology', 'radio', 'number_of_back_camera', 'os'
        ]
    
    @property
    def attributes(self):
        values = [getattr(self, attribute, '') for attribute in self._attributes]

        return zip(self._attributes, values)

    def save(self, *args, **kwargs):
        self.category = Category.objects.get(slug='smart-phone')

        return super().save(*args, **kwargs)

    
