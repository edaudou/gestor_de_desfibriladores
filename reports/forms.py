import django
from django import forms
from .models import Client, Company, Professional, Defibrillator
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class SignUpForm(UserCreationForm):
    required_css_class = 'required'
    email = forms.EmailField(max_length=254,required=True, help_text='Required. Inform a valid email address.', label = "Correo electrónico")
    password1 = forms.CharField(widget=forms.PasswordInput(),required=True, label ="Contraseña")
    password2 = forms.CharField(widget=forms.PasswordInput(),required=True, label ="Confirmar contraseña")

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2',)

class CompanyForm(forms.Form):
    required_css_class = 'required'
    cif = forms.CharField(max_length=9, required=True, label="CIF")
    phone = forms.CharField(max_length=9, required=True, label="Telefono")
    email = forms.EmailField(max_length=254,required=False, help_text='Required. Inform a valid email address.', label = "Correo electrónico")
    address = forms.CharField(max_length=112, required=False, help_text='Optional.', label="Dirección")


    class Meta:
        model = Company
        fields = ('cif', 'phone', 'email', 'address')

class ClientForm(forms.Form):
    required_css_class = 'required'
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.', label="Nombre")
    last_name = forms.CharField(max_length=100, required=False, help_text='Optional.', label="Apellidos")
    nif = forms.CharField(max_length=9, required=True, label="NIF")
    address = forms.CharField(max_length=112, required=False, help_text='Optional.', label="Dirección")
    phone = forms.CharField(max_length=9, required=True, label="Telefono")

    class Meta:
        model = Company
        fields = ('nif', 'phone', 'address', 'first_name', 'last_name')

class loginUserForm(forms.Form):
    required_css_class = 'required'
    email = forms.EmailField(max_length=254,required=True, help_text='Required. Inform a valid email address.', label = "Correo electrónico")
    password1 = forms.CharField(widget=forms.PasswordInput(), required=True,label ="Contraseña")

    class Meta:
        model = User
        fields = ('email', 'password1')   