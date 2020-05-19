from django import forms
from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User
from account.models import Account


class RegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = Account
        fields = ['username', 'email', 'password1', 'password2']
