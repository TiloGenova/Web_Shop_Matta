from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from crispy_forms.helper import FormHelper



class CreateUserForm(UserCreationForm):  #takes basically the django class
    password2 = forms.CharField(label='Conferma Password',
    widget = forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name',
                  'email', 'password1', 'password2']
        labels = {'email': 'Email', 'first_name': 'Nome', 'last_name': 'Cognome', 'password2': 'Conferma Password'}



class ContactForm(forms.Form):
    helper = FormHelper()
    helper.form_show_labels = True

    first_name = forms.CharField(max_length=50, label="Nome:")
    email_address = forms.EmailField(max_length=150, label="Email:", required=True)
    message = forms.CharField(widget=forms.Textarea, label="Messaggio:", max_length=2000, required=True)




