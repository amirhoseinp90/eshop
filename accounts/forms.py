"""Forms for user accounts."""
from typing import Any
from django import forms
from django.contrib.auth import get_user_model
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Div, Submit

User = get_user_model()


class RegisterForm(forms.ModelForm):
    """User Registration form."""
    password = forms.CharField(
        max_length=255, min_length=3, widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name',
                  'password', 'confirm_password')

    def clean(self):
        super().clean()
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')

        if (not password or not confirm_password) or password != confirm_password:
            raise forms.ValidationError(
                'password and confirm password don`t match.')

    def save(self, commit=True):
        """Create a user with encrypted password."""
        user = super().save(commit)
        password = self.cleaned_data.get('password')
        user.set_password(password)

        if commit:
            user.save()
        return user


class AccountVerificationForm(forms.Form):
    """Account verification form."""
    code = forms.CharField(max_length=8)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['code'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'کد تأیید'})


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField()

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if email and password:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                raise forms.ValidationError('کاربری با این مشخصات وجود ندارد.')

            if not user.check_password(password):
                raise forms.ValidationError('کاربری با این مشخصات وجود ندارد.')

            if not user.is_email_verified:
                raise forms.ValidationError(
                    'لطفا ابتدا حساب کاربری خود را فعال کنید.')

        cleaned_data['user'] = user

        return cleaned_data


class PersonalInfoForm(forms.ModelForm):
    email = forms.EmailField(required=False)

    class Meta:
        fields = ('email', 'first_name', 'last_name')
        model = User

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()

        self.fields['email'].help_text = 'درحال حاضر ایمیل قابل تغییر نمیباشد'
        self.fields['email'].widget.attrs.update(
            {'readonly': True, 'disabled': True})
        self.fields['email'].widget.attrs['class'] = 'form-control-plaintext opacity-75'

        self.helper.add_input(Submit('submit', 'ثبت تغییرات', css_class='mt-3'))
        self.helper.layout = Layout(
            Field('email'),
            Div(Field('first_name', 'last_name'), css_class='d-flex justify-content-between')
        )

    def clean(self) -> dict[str, Any]:
        cleaned_data = super().clean()

        if 'email' in cleaned_data:
            del cleaned_data['email']

        return cleaned_data
        

        