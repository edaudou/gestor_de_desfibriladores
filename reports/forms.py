from datetime import datetime
from importlib.metadata import requires
import django
from django import forms
from .models import Client, Company, Professional, Defibrillator, Patch
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class SignUpForm(UserCreationForm):
    required_css_class = 'required'
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Correo electrónico'}),max_length=254,required=True, help_text='Campo requerido. Introduzca una dirección e-mail válida', label = "Correo electrónico")
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña'}),required=True, label ="Contraseña")
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirmar contraseña'}),required=True, label ="Confirmar contraseña")

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2',)

class CompanyForm(forms.Form):
    required_css_class = 'required'
    cif = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'CIF','class':'form__field'}),max_length=9, required=True, label="CIF",error_messages={'required': 'Please enter your cif'})
    company_phone = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Teléfono'}), max_length=9, required=True, label="Telefono")
    company_email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Correo electrónico'}), max_length=254,required=False, help_text='Campo requerido. Introduzca una dirección e-mail válida', label = "Correo electrónico")
    company_address = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Dirección'}), max_length=112, required=False, help_text='Opcional.', label="Dirección")

    class Meta:
        model = Company
        fields = ('cif', 'company_phone', 'company_email', 'company_address')

class ClientForm(forms.Form):
    required_css_class = 'required'
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Nombre'}),max_length=30, required=False, help_text='Opcional.', label="Nombre")
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Apellidos'}),max_length=100, required=False, help_text='Opcional.', label="Apellidos")
    nif = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'NIF'}),max_length=9, required=True, label="NIF", error_messages={'required': 'Please enter your nif'})
    address = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Dirección'}),max_length=112, required=False, help_text='Opcional.', label="Dirección")
    phone = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Teléfono'}),max_length=9, required=True, label="Telefono")

    class Meta:
        model = Client
        fields = ('nif', 'phone', 'address', 'first_name', 'last_name')

class ProfessionalForm(forms.Form):
    required_css_class = 'required'
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Nombre'}), max_length=30, required=False, help_text='Opcional.', label="Nombre")
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Apellidos'}),max_length=100, required=False, help_text='Opcional.', label="Apellidos")
    nif = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'NIF'}), max_length=9, required=True, label="NIF")
    address = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Dirección'}), max_length=112, required=False, help_text='Opcional.', label="Dirección")
    phone = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Teléfono'}), max_length=9, required=True, label="Telefono")

    class Meta:
        model = Professional
        fields = ('nif', 'phone', 'address', 'first_name', 'last_name')


class loginUserForm(forms.Form):
    username = forms.EmailField(max_length=254,required=True, help_text='Campo requerido. Introduzca una dirección e-mail válida', label = "Correo electrónico", widget=forms.TextInput(attrs={'class':'form-field animation a3','placeholder': 'Correo electrónico'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-field animation a4', 'placeholder': 'Contraseña'}), required=True,label ="Contraseña")
    class Meta:
        model = User
        fields = ('username', 'password')   

class DefibrillatorForm(forms.Form):
    # def __init__(self, *args, **kwargs):
    #     user = kwargs.pop('user', None)
    #     print("---form---------", user)
    #     super().__init__(*args, **kwargs)
    #     self.fields['client'].queryset = Professional.objects.get(user=user).defibrillator.all().values_list('client', flat=True).distinct()
    #     print("******************",self.fields['client'])
    required_css_class = 'required'
    model = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Modelo'}),max_length=100, required=False, help_text='Opcional.', label="Modelo")
    brand = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Marca'}),max_length=100, required=False, help_text='Opcional.', label="Marca")
    location = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Ubicación'}),max_length=255, required=False, help_text='Opcional.', label="Ubicación")
    installation_date = forms.DateField(
        widget= forms.DateInput(attrs={'type':'date', 'max':datetime.now().date(), 'placeholder': 'Fecha de instalación'})
    )
    battery_expiration_date = forms.DateField(
        widget= forms.DateInput(attrs={'type':'date', 'min':datetime.now().date(), 'placeholder': 'Expiración de baterias'})
    )
    check_date = forms.DateField(
        widget= forms.DateInput(attrs={'type':'date', 'min':datetime.now().date(), 'placeholder': 'Próxima revisión'})
    )
    
        
    class Meta:
        model =  Defibrillator
        fields = ('model','brand','location','installation_date','battery_expiration_date','client')
        