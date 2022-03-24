from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text

from django.http import HttpResponse

from django.shortcuts import render, redirect

from django.template.loader import render_to_string

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.models import User
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
            form.first_name= form.cleaned_data.get('username')
            user = form.save(commit=False)
            user.is_active = False
            user.username =  cliform.cleaned_data.get('first_name')
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your account'
            print(comform)
            negocio = Company.objects.create(
                cif = comform.cleaned_data.get('cif'),
                phone = comform.cleaned_data.get('phone'),
                email = comform.cleaned_data.get('email'),
                address = comform.cleaned_data.get('address')
            )
            negocio.save()
            cliente = Client.objects.create(
                user = user,
                company = negocio,
                nif = cliform.cleaned_data.get('nif'),
                phone =  cliform.cleaned_data.get('phone'),
                email = cliform.cleaned_data.get('email'),
                first_name = user.username,
                last_name = cliform.cleaned_data.get('last_name'),
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


def loginView(request):
    form = loginUserForm

    if request.method == 'POST':
        form = loginUserForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')

            user = authenticate(request, email=email, password1= password)
            if user is not None:
                auth_login(request, user)
                return redirect('reports:list')
            else:
                messages.info(request,'Usuario o contraseña incorrectos')
    template = 'reports/login.html'
    context = {'form':form,}
    return render(request, template, context)

def activate(request, uidb64, token):
    uid = force_text(urlsafe_base64_decode(uidb64))

    user = User.objects.get(pk=uid)

    if user and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        auth_login(request, user)
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')

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
