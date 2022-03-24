import django
from django import forms
from .models import Client, Company, Professional, Defibrillator
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=30, required=False, help_text='Optional.', label="Nombre")
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.', label = "Correo electrónico")
    password1 = forms.CharField(widget=forms.PasswordInput(), label ="Contraseña")
    password2 = forms.CharField(widget=forms.PasswordInput(), label ="Confirmar contraseña")

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )

class CompanyForm(forms.Form):
    cif = forms.CharField(max_length=9, required=True, label="CIF")

    class Meta:
        model = Company
        fields = ('cif')

class loginUserForm(forms.Form):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.', label = "Correo electrónico")
    password1 = forms.CharField(widget=forms.PasswordInput(), label ="Contraseña")

    class Meta:
        model = User
        fields = ('email', 'password1')   