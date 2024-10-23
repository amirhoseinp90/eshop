"""Database models."""
from datetime import timedelta

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, AbstractUser
from django.conf import settings

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    """Represent user in the system."""
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    # avatar photo
    is_email_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('first_name', 'last_name')

    objects = UserManager()

    def __str__(self):
        return self.first_name + self.last_name + ' ' + self.email
    
    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'
 

class AuthenticateCode(models.Model):
    """Otp code model for user authentication."""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    code = models.CharField(max_length=8)
    email = models.EmailField()
    expiration_time = models.DateTimeField(editable=False)

    def save(self, *args, **kwargs):
        """
        Set default expiration time to specified time in settings.
        by default it`s on hour.
        """
        if not self.expiration_time:
            try:
                expiration_duration = settings.OTP_EXPIRATION_DURATION
            except (AttributeError):
                expiration_duration = timedelta(hours=1)

            self.expiration_time = timezone.now() + expiration_duration

        super().save(*args, **kwargs)

    @property
    def is_expired(self):
        """Check authentication code expiration."""
        return timezone.now() > self.expiration_time


    def __str__(self):
        return f'{self.user} : {self.code}'


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    address = models.TextField()
    province = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    unit = models.CharField(max_length=255)
    building_number = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=255)    

    def __str__(self):
        return f'address of ({self.user})'
