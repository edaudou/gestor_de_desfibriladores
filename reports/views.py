from django.shortcuts import render, redirect
from .forms import ClientForm
from django.contrib.auth import authenticate
from .forms import SignUpForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login

# Create your views here.

def index(request):
    form = SignUpForm
    clientForm = ClientForm

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.first_name= form.cleaned_data.get('username')
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            auth_login(request, user)
            return redirect('reports:defibrillator_list')
    else:
        form = SignUpForm()
    context = {
        'form': form,       
    }
    return render(request,'reports/index.html',context)

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
