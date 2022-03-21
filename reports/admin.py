from django.contrib import admin
from . models import Defibrillator, Company, Professional, Client, Patch

admin.site.register(Company)
admin.site.register(Client)
admin.site.register(Professional)
admin.site.register(Patch)
admin.site.register(Defibrillator)