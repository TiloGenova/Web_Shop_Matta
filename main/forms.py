from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Contact



class CreateUserForm(UserCreationForm):  #takes basically the django class
    password2 = forms.CharField(label='Conferma Password',
    widget = forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name',
                  'email', 'password1', 'password2']
        labels = {'email': 'Email', 'first_name': 'Nome', 'last_name': 'Cognome', 'password2': 'Conferma Password'}



class ContactForm(forms.Form):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    email_address = forms.EmailField(max_length=150, required=True)
    message = forms.CharField(widget=forms.Textarea, max_length=2000, required=True)


'''
class ContactForm(forms.Form):
    class Meta:
        model = Contact
        fields = ['first_name', 'last_name', 'email', 'message']

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'input'}),
            'last_name': forms.TextInput(attrs={'class': 'input'}),
            'email': forms.EmailInput(attrs={'class': 'input'}),
            'message': forms.TextInput(attrs={'class': 'input'})
        }'''


