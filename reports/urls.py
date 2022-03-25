from django.urls import path
from django.conf.urls import url
from .views import *

app_name= 'reports'
urlpatterns = [
    path('', index, name='index'),
    path('detail/<int:defibrilator_id>/', defibrillatorDetail, name='defibrillator_detail'),
    path('list/', defibrillatorList, name='defibrillator_list'),
    path('profile/<int:user_id>/', profile, name='profile'),
    path('activate/<uidb64>/<token>',activate, name='activate'),
    path('login/',loginView, name='login'),
    path('logout/',logoutView, name='logout'),

]