from django.urls import path
from account.views import *

app_name='account'

urlpatterns=[
    path('register', register, name='register'),
    path('edit', edit_profile, name='edit_profile'),
    path('set_password/', set_password, name='set_password'),
    path('logout_user/', logout_user, name='logout'),
    path('main/account/', login , name='account'),
]