from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm



class CreateUserForm(UserCreationForm):  #takes basically the django class
    password2 = forms.CharField(label='Conferma Password',
    widget = forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name',
                  'email', 'password1', 'password2']
        labels = {'email': 'Email', 'first_name': 'Nome', 'last_name': 'Cognome', 'password2': 'Conferma Password'}
#