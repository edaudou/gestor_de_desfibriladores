from ctypes.wintypes import INT
from multiprocessing import context
from re import template
from xmlrpc.client import DateTime
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text

from django.http import HttpResponse
from datetime import datetime, timedelta
from django.shortcuts import render, redirect

from django.template.loader import render_to_string

from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages

from django.core.mail import EmailMessage

from .tokens import account_activation_token
from .models import Client, Company, Defibrillator, Patch, Professional
from .forms import SignUpForm, loginUserForm, CompanyForm, ClientForm, ProfessionalForm, DefibrillatorForm

# Create your views here.

def index(request):
    form = SignUpForm
    companyform = CompanyForm
    clientform = ClientForm
    proform = ProfessionalForm

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        comform = CompanyForm(request.POST)
        cliform = ClientForm(request.POST)
        proform = ProfessionalForm(request.POST)

        #request.user.client.(company/desf)_set.all()
        #request.user.professional.desf_set.all()

        if form.is_valid() and comform.is_valid() and cliform.is_valid():
            user = form.save(commit=False)
            
            user.username =  form.cleaned_data.get('email')
            
            user.first_name = cliform.cleaned_data.get('first_name')
            user.last_name = cliform.cleaned_data.get('last_name')

            if user.first_name is not None:
                user.first_name.capitalize()
            if user.last_name is not None:
                user.last_name .capitalize()

            user.is_active = False
            try:
              user.save()
            except:
                return HttpResponse("El usuario ya existe")
            
            current_site = get_current_site(request)
            mail_subject = 'Activate your account'
            print(comform)
            negocio = Company.objects.create(
                cif = comform.cleaned_data.get('cif'),
                phone = comform.cleaned_data.get('company_phone'),
                email = comform.cleaned_data.get('company_email'),
                address = comform.cleaned_data.get('company_address')
            )
            negocio.save()
            cliente = Client.objects.create(
                user = user,
                company = negocio,
                nif = cliform.cleaned_data.get('nif'),
                phone =  cliform.cleaned_data.get('phone'),
                email = form.cleaned_data.get('email'),
                first_name = user.first_name,
                last_name = user.last_name,
                address = cliform.cleaned_data.get('address'),
            )
            cliente.save()
            message = render_to_string('reports/acc_active_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user)
            })

            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()

            return HttpResponse('Por favor, confirma tu dirección de correo electrónico para completar el registro.')
        elif form.is_valid() and proform.is_valid():
            user = form.save(commit=False)
            
            user.username =  form.cleaned_data.get('email')
            
            user.first_name = proform.cleaned_data.get('first_name')
            user.last_name = proform.cleaned_data.get('last_name')

            if user.first_name is not None:
                user.first_name.capitalize()
            if user.last_name is not None:
                user.last_name .capitalize()

            user.is_active = False
            try:
              user.save()
            except:
                return HttpResponse("El usuario ya existe")
            
            current_site = get_current_site(request)
            mail_subject = 'Activate your account'
            print(proform)
            

            profesional = Professional.objects.create(
                user = user,
                nif = proform.cleaned_data.get('nif'),
                phone =  proform.cleaned_data.get('phone'),
                email = form.cleaned_data.get('email'),
                first_name = user.first_name,
                last_name = user.last_name,
                address = proform.cleaned_data.get('address'),
                is_pro = True,
            )
            profesional.save()
            message = render_to_string('reports/acc_active_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user)
            })

            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()

            return HttpResponse('Por favor, confirma tu dirección de correo electrónico para completar el registro.')

    else:
        form = SignUpForm()
    context = {
        'form': form,    
        'companyform': companyform,
        'clientform': clientform,  
        'proform': proform, 
    }
    return render(request,'reports/index.html',context)

def logoutView(request):
    logout(request)
    return redirect('reports:login')

class LoginUser(LoginView):
    template_name = 'reports/login.html'

    def dispatch(self, request, *args, **kwargs):  
        if request.user.is_authenticated:
            return redirect( 'reports:defibrillator_list' )

        user=authenticate(email=request.POST.get('email'),password1=request.POST.get('password1'))
        print(request.POST.get('email'))
        print(request.POST.get('password1'))
        if user is  None:            
            messages.info(request,'El usuario o contraseña es incorrecto')     
        

        return super().dispatch(request, *args, **kwargs)     

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = loginUserForm
        return context

def loginView(request):
    form = loginUserForm
    template = 'reports/login.html'
    context = {'form':form,}
    if request.method == 'POST':
        form = loginUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password= password)
            if user is not None:
                auth_login(request, user)
                return redirect('reports:defibrillator_list')
            else:
                messages.info(request,'Usuario o contraseña incorrectos')
                return redirect('reports:login')

 
    return render(request, template, context)

def activate(request, uidb64, token):
    uid = force_text(urlsafe_base64_decode(uidb64))

    user = User.objects.get(pk=uid)

    if user and account_activation_token.check_token(user, token):
        user.is_active = True
        now = datetime.now()
        created = user.date_joined + timedelta(hours=2)
        created = created.replace(tzinfo=None)
        if now-timedelta(hours=24) <= created <= now+timedelta(hours=24):
            user.save()
            auth_login(request, user)
            return HttpResponse('Gracias por confirmar el correo. Le hemos iniciado sesión.')
        else:
            return HttpResponse('Han pasado más de 24h')
    else:
        return HttpResponse('El link de activación es inválido')

@login_required(login_url='/')
def profile(request):
    return render(request,'reports/profile.html',{})

@login_required(login_url='/')
def clientList(request):
    pro = Professional.objects.get(user=request.user)
    clientes = pro.defibrillator.all().values_list('client', flat=True).distinct()
    print(clientes)
    context= {}
    return render(request,'reports/clients.html',context)
@login_required(login_url='/')
def defibrillatorList(request):
    form = DefibrillatorForm
    list=[]
    try:
        person = Client.objects.get(user = request.user)
        list = person.defibrillator.all()
    except:
        person = Professional.objects.get(user = request.user)
        list = person.defibrillator.all()
    
    if request.method == 'POST':
        form = DefibrillatorForm(request.POST)
        # print(Client.objects.get(user= request.user))

        if form.is_valid():
            print("no soy un inválido")
            defibrilator_object = Defibrillator.objects.create(
                model =  form.cleaned_data.get('model'),
                brand =  form.cleaned_data.get('brand'),
                location = form.cleaned_data.get('location'),
                installation_date  =  form.cleaned_data.get('installation_date'),
                battery_expiration_date =  form.cleaned_data.get('battery_expiration_date'),
                check_date =  form.cleaned_data.get('check_date'),
            )
            if person.is_pro:
                defibrilator_object.professional.set([person]) #Al ser manyToMany hay en lugar de asignar un valor se hace set de una lista de valores, aunque solo necesitemos pasar uno ahora
            defibrilator_object.save()
            print("guardado")
            return redirect("/list")
        else:
            print("NOPE")
    form = DefibrillatorForm
    print(list)
    context= {
        "defibrillatorList" : list,
        "form" : form,
        'person' :person,
    }
    return render(request,'reports/listview.html',context)

@login_required(login_url='/')
def defibrillatorDetail(request,defibrillator_id):
    d = Defibrillator.objects.get(pk=defibrillator_id)
    patchs = Patch.objects.filter(defibrillator_id= d)
    form = DefibrillatorForm
    context={
        "detail": d,
        'patchs': patchs,
        "form": form,
    }
    return render(request,'reports/detailview.html',context)

def error_404(request, exception):
    return render(request, '404.html')

import asyncio
from asgiref.sync import sync_to_async

# @sync_to_async
# def check_activation():
#     not_actived_users = User.objects.filter(is_active = False)
#     print(not_actived_users)
#     await asyncio.sleep(28800) #loop 8 hours
    
# asyncio.run(check_activation())