"""Tests for forms."""
from django.test import TestCase
from accounts.forms import RegisterForm


class TestUserAuthforms(TestCase):
    """Test user authentication forms."""
    def test_confirm_password_validator(self):
        """Test password and confirm password must be same."""
        payload = {
            'email': 'test@example.com',
            'full_name': 'test full name',
            'password': 'testpass123',
            'confirm_password': 'diffpass123'
        }

        form = RegisterForm(payload)

        self.assertFormError(form, field=None, errors='password and confirm password don`t match.')
        self.assertFalse(form.is_valid())




