from email.policy import default
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django_currentuser.middleware import get_current_authenticated_user




class Contact(models.Model):
    address = models.CharField(verbose_name='Dirección', max_length=255, null = True, blank=True)
    email = models.CharField(verbose_name='E-mail', max_length=100, null = True, blank=True)
    phone = models.CharField(verbose_name='Teléfono', max_length=9)
    class Meta:
        abstract = True

class Person(Contact):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(verbose_name='Nombre',max_length=100, null = True, blank=True)
    last_name = models.CharField(verbose_name='Apellidos',max_length=255, null = True, blank=True)
    nif = models.CharField(verbose_name='NIF', max_length=9,)
    created_at = models.DateTimeField(auto_now_add=True, null = True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null = True, blank=True)
    is_pro =  models.BooleanField(default = False)
    class Meta:
        abstract = True
    def save(self, *args, **kwargs):
        self.product_type = 'Contact'
        return super(Contact, self).save(*args, **kwargs)
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Company(Contact):
    id = models.AutoField(verbose_name='ID', primary_key=True)
    cif = models.CharField(verbose_name='cif', max_length=9,)
    def save(self, *args, **kwargs):
        self.product_type = 'Contact'
        return super(Contact, self).save(*args, **kwargs)

class Professional(Person):
    id = models.AutoField(verbose_name='ID', primary_key=True)
    def __str__(self):
        return f"{self.email}"

# Un cliente es el representante de la empresa que posee los desfibriladores
class Client(Person):
    id = models.AutoField(verbose_name='ID', primary_key=True)
    company = models.OneToOneField(Company, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, related_name="pro_creator", on_delete= models.PROTECT,null = True)
    
    def save(self, *args, **kwargs):
        self.product_type = 'Person'       
        return super(Person, self).save(*args, **kwargs)
    def __str__(self):
        return f"{self.email}"

class Defibrillator(models.Model):
    id = models.AutoField(verbose_name='ID', primary_key=True)
    # Nombre del modelo
    model = models.CharField(verbose_name='Modelo', max_length=100, null = True, blank=True)
    brand = models.CharField(verbose_name='Marca', max_length=100, null = True, blank=True)
    location = models.CharField(verbose_name='Localización', max_length=255, null = True, blank=True)
    # Propietario -> cliente? user? sin mas un nombre de una empresa?
    client = models.ForeignKey(Client,  on_delete=models.CASCADE, related_name="%(class)s")
    installation_date = models.DateTimeField( null = True, blank=True)
    # Fecha caducidad del parche o parches -> otro model? -> habrá que crear un objeto parche que tenga atributo fecha de caducidad para reflejarlo aquí
    # Fecha caducidad de la bateria
    battery_expiration_date = models.DateTimeField(null = True, blank=True)
    check_date = models.DateTimeField(null = True, blank=True)
    professional = models.ManyToManyField(Professional, related_name="%(class)s", blank=True)
    #Para almacenar en postgis y luego representarlo en la api de google maps
    longitude = models.CharField(verbose_name="Longitud",max_length=50, null=True, blank=True)
    latitude = models.CharField(verbose_name="Latitud",max_length=50, null=True, blank=True)

class Patch(models.Model):
    id = models.AutoField(verbose_name='ID', primary_key=True)
    expiration_date =  models.DateTimeField(verbose_name='Fecha de expiración', null = True, blank=True)
    defibrillator = models.ForeignKey(Defibrillator,  on_delete=models.CASCADE, related_name="%(class)s", null = True, blank=True)