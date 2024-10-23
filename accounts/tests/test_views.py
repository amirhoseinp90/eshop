"""Test for views."""
from http import HTTPStatus
import json

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from accounts.forms import RegisterForm
from accounts.models import AuthenticateCode
from utils.test import create_user


User = get_user_model()


HOME_URL = reverse('home:home')

# AUTH urls
REGISTER_URL = reverse('accounts:register')
ACCOUNT_VERIFICATION_URL = reverse('accounts:account-verification')


class TestUserAuthViews(TestCase):
    """Test user authentication views."""

    def test_get_register_successful(self):
        """Test getting register is successful."""
        res = self.client.get(REGISTER_URL)

        self.assertEqual(res.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(res, 'accounts/register.html')
        self.assertIsInstance(res.context['form'], RegisterForm)

    def test_get_register_authorized_request(self):
        """Test getting register view with authorized requests results in an Redirect."""
        user = create_user()
        self.client.force_login(user)

        res = self.client.get(REGISTER_URL)

        self.assertRedirects(res, HOME_URL)
    
    def test_post_register_view_successful(self):
        """Test posting register view is successful."""
        payload = {
            'email': 'test@example.com',
            'full_name': 'test full name',
            'password': 'testpass123',
            'confirm_password': 'testpass123'
        }

        res = self.client.post(REGISTER_URL, payload)

        self.assertEqual(res.status_code, HTTPStatus.OK)
        users = User.objects.all()
        self.assertEqual(users.count(), 1)
        user = users.first()
        self.assertEqual(user.email, payload['email'])
        self.assertTrue(user.check_password(payload['password']))
        
        self.assertIn('_auth_verify_user_pk', self.client.session)
        self.assertEqual(self.client.session['_auth_verify_user_pk'], user.pk)
        
    def test_post_register_view_send_email(self):
        """Test after successfuly posting register an authentication code will send."""
        self.skipTest('in progress...')
    
    def test_post_register_bad_request(self):
        """Test posting registe with invalid credentials will fails."""
        payload = {
            'email': 'bad email',
            'full_name': '',
            'password': 'testpass123',
            'confirm_password': 'diffpass123'
        }

        res = self.client.post(REGISTER_URL, payload)

        self.assertEqual(res.status_code, HTTPStatus.BAD_REQUEST)
        self.assertFalse(User.objects.all().exists())
        self.assertNotIn('_auth_verify_user_pk', self.client.session)

    def test_post_register_with_email_exists(self):
        """Test posting register with an email address that is already exists."""
        email = 'exists@example.com'
        user = create_user(email=email)
        payload = {
            email:email,
            'full_name': 'test full name',
            'password': 'testpass123',
            'confirm_password': 'testpass123'
        }

        res = self.client.post(REGISTER_URL, payload)

        self.assertEqual(res.status_code, HTTPStatus.BAD_REQUEST)
        users = User.objects.all()
        self.assertEqual(users.count(), 1)
        self.assertEqual(user, users.first())

    def test_get_account_verification_empty_session(self):
        """Test getting account verification with empty session results in an redirect."""
        res = self.client.get(ACCOUNT_VERIFICATION_URL)
        
        self.assertRedirects(res, HOME_URL)

    def test_get_account_verification_authorized_request(self):
        """Test getting account verification with authorized request will fail."""
        user = create_user()
        session = self.client.session
        session['_auth_verify_user_pk'] = user.pk
        session.save()
        self.client.force_login(user)
        
        res = self.client.get(ACCOUNT_VERIFICATION_URL)
        
        self.assertRedirects(res, HOME_URL)

    def test_get_account_verification_successful(self):
        """Test getting account verification with valid sessions."""
        user = create_user()
        session = self.client.session
        session['_auth_verify_user_pk'] = user.pk
        session.save()    
        
        res = self.client.get(ACCOUNT_VERIFICATION_URL)
        
        self.assertEqual(res.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(res, 'accounts/account_verification.html')
    
    def test_post_account_verificatoin_successful(self):
        """Test posting account verification with valid auth code."""
        user = create_user()
        AuthenticateCode.objects.create(user=user, code='1234567')
        session = self.client.session
        session['_auth_verify_user_pk'] = user.pk
        session.save()
        
        payload = {'code': '1234567'}    
        res = self.client.post(ACCOUNT_VERIFICATION_URL, payload)        
        
        self.assertEqual(res.status_code, HTTPStatus.OK)
    
    def test_post_account_verification_invalid_auth_code(self):
        """Test posting account verification with invalid auth code."""
        user = create_user()
        AuthenticateCode.objects.create(user=user, code='1234567')
        session = self.client.session
        session['_auth_verify_user_pk'] = user.pk
        session.save()
        
        payload = {'code': '7654321'}
        res = self.client.post(ACCOUNT_VERIFICATION_URL, payload)
        
        self.assertEqual(res.status_code, HTTPStatus.BAD_REQUEST)
    
        