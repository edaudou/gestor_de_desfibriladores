import django
from django import forms
from .models import Client, Company, Professional, Defibrillator
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class SignUpForm(UserCreationForm):
    required_css_class = 'required'
    email = forms.EmailField(max_length=254,required=True, help_text='Campo requerido. Introduzca una dirección e-mail válida', label = "Correo electrónico")
    password1 = forms.CharField(widget=forms.PasswordInput(),required=True, label ="Contraseña")
    password2 = forms.CharField(widget=forms.PasswordInput(),required=True, label ="Confirmar contraseña")

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2',)

class CompanyForm(forms.Form):
    required_css_class = 'required'
    cif = forms.CharField(max_length=9, required=True, label="CIF")
    company_phone = forms.CharField(max_length=9, required=True, label="Telefono")
    company_email = forms.EmailField(max_length=254,required=False, help_text='Campo requerido. Introduzca una dirección e-mail válida', label = "Correo electrónico")
    company_address = forms.CharField(max_length=112, required=False, help_text='Opcional.', label="Dirección")

    class Meta:
        model = Company
        fields = ('cif', 'company_phone', 'company_email', 'company_address')

class ClientForm(forms.Form):
    required_css_class = 'required'
    first_name = forms.CharField(max_length=30, required=False, help_text='Opcional.', label="Nombre")
    last_name = forms.CharField(max_length=100, required=False, help_text='Opcional.', label="Apellidos")
    nif = forms.CharField(max_length=9, required=True, label="NIF")
    address = forms.CharField(max_length=112, required=False, help_text='Opcional.', label="Dirección")
    phone = forms.CharField(max_length=9, required=True, label="Telefono")

    class Meta:
        model = Company
        fields = ('nif', 'phone', 'address', 'first_name', 'last_name')

class loginUserForm(forms.Form):
    required_css_class = 'required'
    username = forms.EmailField(max_length=254,required=True, help_text='Campo requerido. Introduzca una dirección e-mail válida', label = "Correo electrónico")
    password = forms.CharField(widget=forms.PasswordInput(), required=True,label ="Contraseña")

    class Meta:
        model = User
        fields = ('username', 'password')   