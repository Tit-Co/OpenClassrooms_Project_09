from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect

from home.forms import LoginForm, SigninForm
from home.models import User


def index(request):
    if request.method == 'POST':
        login_form  = LoginForm(request.POST)
        if login_form.is_valid():
            user = authenticate(
                username=login_form.cleaned_data['username'],
                password=login_form.cleaned_data['password']
            )
            if user:
                login(request, user)
                messages.success(request, "Connexion réussie.")
                return redirect('feed:feed')
            else:
                print("Authentication failed !")
                messages.error(request, "Identifiants incorrects.")
    else:
        login_form = LoginForm()

    return render(request, 'home/index.html', {'login_form': login_form})

def sign_in(request):
    if request.method == 'POST':
        signin_form = SigninForm(request.POST)
        if signin_form.is_valid():
            user = User.objects.create_user(
                username=signin_form.cleaned_data['username'],
                password=signin_form.cleaned_data['password']
            )
            login(request, user)
            messages.success(request, "Inscription réussie. Vous êtes maintenant connecté.")
            return redirect('feed:feed')
        else:
            messages.error(request, "L'inscription a échoué. Veuillez réessayer.")
    else:
        signin_form = SigninForm()

    return render(request, 'home/sign_in.html', {'signin_form': signin_form})
