from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect

from account.forms import LoginForm


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

    return render(request, 'core/index.html', {'login_form': login_form})
