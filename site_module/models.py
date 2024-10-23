from django.db import models

class Slider(models.Model):
    title = models.CharField(max_length=200, null=True, blank=True, verbose_name='عنوان')
    url = models.URLField(max_length=500, null=True, blank=True, verbose_name='لینک')
    url_title = models.CharField(max_length=200, null=True, blank=True, verbose_name='عنوان لینک')
    description = models.TextField(null=True, blank=True, verbose_name='توضیحات اسلایدر')
    image = models.ImageField(upload_to='images/sliders', verbose_name='تصویر اسلایدر')
    is_active = models.BooleanField(default=True, verbose_name='فعال / غیرفعال')

    def __str__(self):
        return self.title or 'slider'
