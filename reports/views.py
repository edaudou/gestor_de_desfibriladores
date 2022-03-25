from re import template
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text

from django.http import HttpResponse

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
from .models import Client, Company
from .forms import SignUpForm, loginUserForm, CompanyForm, ClientForm

# Create your views here.

def index(request):
    form = SignUpForm
    companyform = CompanyForm
    clientform = ClientForm

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        comform = CompanyForm(request.POST)
        cliform = ClientForm(request.POST)

        if form.is_valid() and comform.is_valid() and cliform.is_valid():
            user = form.save(commit=False)
            
            user.username =  form.cleaned_data.get('email')
            
            user.first_name = cliform.cleaned_data.get('first_name').capitalize()
            print("****",user)
            user.is_active = False
            try:
                user.save()
            except:
                print("usuario ya existe")
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
                last_name = cliform.cleaned_data.get('last_name').capitalize(),
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

            return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = SignUpForm()
    context = {
        'form': form,    
        'companyform': companyform,
        'clientform': clientform,   
    }
    return render(request,'reports/index.html',context)

def logoutView(request):
    logout(request)
    return redirect('reports:index')

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
            print("\n VÁLIDO")

            user = authenticate(username=username, password= password)
            print(password)
            if user is not None:
                print("\n Todo gucci")
                            
                auth_login(request, user)
                return redirect('reports:defibrillator_list')
            else:
                print("\n Usuario incorrecto")

                messages.info(request,'Usuario o contraseña incorrectos')
                return redirect('reports:login')

 
    return render(request, template, context)

def activate(request, uidb64, token):
    uid = force_text(urlsafe_base64_decode(uidb64))

    user = User.objects.get(pk=uid)

    if user and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        auth_login(request, user)
        return HttpResponse('Gracias por confirmar el correo. Le hemos iniciado sesión.')
    else:
        return HttpResponse('El link de activación es inválido')

@login_required(login_url='index')
def profile(request):
    return render(request,'reports/profile.html',{})

@login_required(login_url='index')
def defibrillatorList(request):
    return render(request,'reports/listview.html',{})

@login_required(login_url='index')
def defibrillatorDetail(request):
    return render(request,'reports/detailview.html',{})

def error_404(request, exception):
    return render(request, '404.html')
