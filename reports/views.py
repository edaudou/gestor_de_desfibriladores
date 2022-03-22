from django.shortcuts import render
from .forms import ClientForm
from django.contrib.auth.decorators import login_required

# Create your views here.

def index(request):
    clientForm = ClientForm
    context = {
        'clientForm': clientForm,
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
