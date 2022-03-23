from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from .forms import SignUpForm
from django.utils.encoding import force_bytes, force_text
from django.http import HttpResponse

from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import EmailMessage
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model


# Create your views here.

def index(request):
    form = SignUpForm

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.first_name= form.cleaned_data.get('username')
            user = form.save(commit=False)
            user.is_active = False
            # user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your account'
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
    }
    return render(request,'reports/index.html',context)

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))

        user = User.objects.get(pk=uid)

    except Exception as e:
        user = None

    if user and account_activation_token.check_token(user, token):
        user.save()


        auth_login(request, user)
        # return redirect('home')
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
