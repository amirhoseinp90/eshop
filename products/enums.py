from django.db import models

class Capacity(models.TextChoices):
    MB_512 = '512 مگابایت'
    GB_1 = '1 گیگابایت'
    GB_2 = '2 گیگابایت'
    GB_4 = '4 گیگابایت'
    GB_6 = '6 گیگابایت'
    GB_8 = '8 گیگابایت'
    GB_12 = '12 گیگابایت'
    GB_16 = '16 گیگابایت'
    GB_32 = '32 گیگابایت'
    GB_64 = '64 گیگابایت'
    GB_128 = '128 گیگابایت'
    GB_256 = '256 گیگابایت'
    GB_512 = '512 گیگابایت'
    
class ScreenTechnology(models.TextChoices):
    LED = 'LED'
    OLED = 'OLED'
    AMOLED = 'AMOLED'
    SUPER_AMOLED = 'SUPER AMOLED'
    SUPER_RETINA = 'SUPER RETINA'


class RefreshRate(models.TextChoices):
    HZ_30 = '30 هرتز'
    HZ_60 = '60 هرتز'
    HZ_120 = '120 هرتز'
    HZ_240 = '240 هرتز'


class CameraNumber(models.TextChoices):
    num_1 = '1 ماژول دوربین'
    num_2 = '2 ماژول دوربین'
    num_3 = '3 ماژول دوربین'
    num_4 = '4 ماژول دوربین'
    num_5 = '5 ماژول دوربین'
    num_6 = '6 ماژول دوربین'

class OS(models.TextChoices):
    IOS = 'ios'
    ANDROID = 'android'
    WINDOWS_PHONE = 'windows phone'

