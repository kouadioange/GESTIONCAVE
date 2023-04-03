
from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('inscription/', inscription, name='inscription'),
    path('liste_user/', liste_user, name='liste_user'),
    path('login/', loginPage, name='login'),
    path('logout/', logoutUser, name='logoutUser'),
    #path('permission_user/', permission_user, name='permission_user'),

]
