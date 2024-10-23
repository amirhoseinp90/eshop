"""Managers for model."""
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import AbstractUser


class UserManager(BaseUserManager):
    """Custom user manager."""

    def _create_user(self, email, first_name, last_name, password=None, **extra_fields):
        """Create, save and return a user with encrypted password."""
        if not email:
            raise ValueError('email cannot be empty.')
    
        if not first_name:
            raise ValueError('first name cannot be empty')
        
        if not last_name:
            raise ValueError('last name cannot be empty')
        
        user = self.model(email=self.normalize_email(email), first_name=first_name, last_name=last_name, **extra_fields)
        user.set_password(password)

        user.save()
        return user
    
    def create_user(self, email, first_name, last_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        return self._create_user(email, first_name, last_name, password, **extra_fields)
    
    def create_superuser(self, email, first_name, last_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_email_verified', True)

        return self._create_user(email, first_name, last_name, password, **extra_fields)