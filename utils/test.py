"""Utility functions for testing purpose."""
from django.contrib.auth import get_user_model


User = get_user_model()


def create_user(**params):
    """Create, save and return a new user."""
    params.setdefault('email', 'test@example.com')
    params.setdefault('full_name', 'test fullname')
    params.setdefault('password', 'testpass123')

    return User.objects.create_user(**params)
    
