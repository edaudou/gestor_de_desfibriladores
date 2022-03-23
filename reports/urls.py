from django.urls import path
from .views import *

app_name= 'reports'
urlpatterns = [
    path('', index, name='index'),
    path('detail/<int:defibrilator_id>/', defibrillatorDetail, name='defibrillator_detail'),
    path('list/', defibrillatorList, name='defibrillator_list'),
    path('profile/<int:user_id>/', profile, name='profile'),
]