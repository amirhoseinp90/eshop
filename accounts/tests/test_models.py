"""Test for models."""
from datetime import timedelta, datetime
from unittest.mock import patch

from django.test import TestCase, override_settings
from django.utils import timezone
from django.contrib.auth import get_user_model

from accounts.models import AuthenticateCode
from utils.test import create_user


User = get_user_model()


class TestModels(TestCase):
    """Test models."""

    def test_create_user_with_email_successful(self):
        """Test creating a user with an email address is successful."""
        payload = {
            'email': 'test@example.com',
            'full_name': 'test full_name',
            'password': 'testpass123'
        }

        user = User.objects.create_user(**payload)

        self.assertEqual(str(user), user.full_name)
        self.assertEqual(user.email , payload['email'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertFalse(user.is_email_verified)

    def test_new_user_email_normalized(self):
        """Test email is normalized for new users."""
        sample_email = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.COM', 'TEST3@example.com'],
        ]

        for email, expected in sample_email:
            user = User.objects.create_user(
                email=email,
                full_name='test name'
            )
            self.assertEqual(user.email, expected)

            user.delete() # prevent email unique constrained fail.

    def test_create_user_without_email_raises_error(self):
        """Test creating a user without an email address raises a ValueError."""
        payload = {
            'email': '',
            'full_name': 'test full_name',
        }

        with self.assertRaises(ValueError):
            user = User.objects.create_user(**payload)
    
    def test_create_superuser(self):
        """Test creating a superuser."""
        payload = {
            'email': 'test@example.com',
            'full_name': 'test full_name'
        }

        user = User.objects.create_superuser(**payload)

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_authenticate_code(self):
        """Test creating authenticate code for user is successful."""
        user = create_user()

        auth_code = AuthenticateCode.objects.create(
            user=user,
            code=54321
        )

        self.assertEqual(str(auth_code), f'{auth_code.user} : {auth_code.code}')
    
    @patch('accounts.models.timezone.now')
    @override_settings(OTP_EXPIRATION_DURATION=timedelta(hours=3))
    def test_create_authenticate_code_with_expiration_duration(self, mocked_timezone_now):
        """
        Test creating an authentication code with specified
        expiration duration is successful.
        """
        datetime_now = datetime.now()
        mocked_timezone_now.return_value = datetime_now

        user = create_user()
        auth_code = AuthenticateCode.objects.create(
            user=user,
            code=54321
        )

        self.assertEqual(auth_code.expiration_time, datetime_now + timedelta(hours=3))

    @override_settings(OTP_EXPIRATION_DURATION=timedelta(hours=1))
    def test_authenticate_code_is_expired_successful(self):
        """Test authentication code is_expired is true."""
        user = create_user()

        auth_code = AuthenticateCode.objects.create(
            user=user,
            code=54321,
        )

        auth_code.expiration_time = timezone.now() - timedelta(hours=1, minutes=1)

        self.assertTrue(auth_code.is_expired)
    

    @override_settings(OTP_EXPIRATION_DURATION=timedelta(hours=1))
    def test_authenticate_code_is_expired_failes(self):
        """Test authentication code is_expired is false."""
        user = create_user()

        auth_code = AuthenticateCode.objects.create(
            user=user,
            code=54321
        )

        self.assertFalse(auth_code.is_expired)

        
        

        


    


        
