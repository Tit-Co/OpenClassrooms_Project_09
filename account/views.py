from django.contrib.auth import login, logout
from django.contrib import messages
from django.shortcuts import render, redirect

from account.forms import SignupForm
from account.models import User


def sign_up(request):
    if request.method == 'POST':
        signup_form = SignupForm(request.POST)
        if signup_form.is_valid():
            user = User.objects.create_user(
                username=signup_form.cleaned_data['username'],
                password=signup_form.cleaned_data['password']
            )
            login(request, user)
            messages.success(request, "Inscription réussie. Vous êtes maintenant connecté.")
            return redirect('feed:feed')
        else:
            messages.error(request, "L'inscription a échoué. Veuillez réessayer.")
    else:
        signup_form = SignupForm()

    return render(request, 'account/sign_up.html', {'signup_form': signup_form})

def log_out(request):
    logout(request)
    messages.success(request, "Deconnexion réussie.")
    return redirect('index')