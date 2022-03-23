from django.urls import path
from django.conf.urls import url
from .views import *

app_name= 'reports'
urlpatterns = [
    path('', index, name='index'),
    path('detail/<int:defibrilator_id>/', defibrillatorDetail, name='defibrillator_detail'),
    path('list/', defibrillatorList, name='defibrillator_list'),
    path('profile/<int:user_id>/', profile, name='profile'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,40})/$', activate, name='activate'),
]