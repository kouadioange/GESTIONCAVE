from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User, Group
from .forms import *
from django.http import HttpResponse
from django.contrib import messages
# Create your views here.


"""@staff_member_required
def permission_user(request):
    if request.method == 'POST':
        if 'permission' in request.POST:
            utilisateur = request.POST.get('utilisateur')
            id_obj = User.objects.get(id=utilisateur)
            permi = request.POST.get('status')

            group = Group.objects.get(name=permi)
            request.user.groups.add(group)

            messages.success(request, 'ajouter avec succes')
    return render(request,'compte/inscription.html')
"""

def loginPage(request):
    if request.method == 'POST':
        if 'connexion' in request.POST:
            username = request.POST.get('username')
            mdp = request.POST.get('mdp')
            user = authenticate(request, username=username, password=mdp)
            if user is not None:
                login(request,user)
                return redirect('accueil')
            else:
                messages.error(request, "Nom d'utilisateur Introuvable")
                return redirect('login')

    return render(request, 'compte/login.html')


def inscription(request):
    us = User.objects.all()
    if request.method == 'POST':
        if 'enregistrer' in request.POST:
            username = request.POST.get('username')
            email = request.POST.get('email')
            mdp1 = request.POST.get('mdp1')
            mdp2 = request.POST.get('mdp2')

            if mdp1 == mdp2:
                formulaire = User.objects.create_user(
                    username=username,
                    email=email,
                    password=mdp1,
                )
                messages.success(request, 'Inscription réussie !!!')
            else:
                messages.error(request, 'Inscription Echouée, Mot de passe Différent')
    context = {
        'us': us,
    }
    return render(request, 'compte/inscription.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


def liste_user(request):

    context = {
    }
    return render(request, 'compte/liste_user.html', context)

