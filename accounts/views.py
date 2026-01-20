from django.contrib.auth import login, logout
from django.contrib import messages
from django.shortcuts import render, redirect


from accounts.forms import SignupForm, LoginForm


def log_in(request):
    if request.method == 'POST':
        login_form  = LoginForm(request, data=request.POST)
        if login_form.is_valid():
            user = login_form.get_user()
            login(request, user)
            messages.success(request, f"{user}, connexion réussie.")
            return redirect('feed:feed')
        else:
            messages.error(request, "Identifiants incorrects.")
    else:
        login_form = LoginForm()

    return render(request, 'accounts/index.html', {'login_form': login_form})

def sign_up(request):
    if request.method == "POST":
        signup_form = SignupForm(request.POST)
        if signup_form.is_valid():
            user = signup_form.save()
            login(request, user)
            messages.success(request, f"{user}, inscription réussie. Vous êtes maintenant connecté.")
            return redirect('feed:feed')
        else:
            messages.error(request, "L'inscription a échoué. Veuillez réessayer.")
    else:
        signup_form = SignupForm()

    return render(request, 'accounts/sign_up.html', {'signup_form': signup_form})

def log_out(request):
    logout(request)
    messages.success(request, "Deconnexion réussie.")
    return redirect('log-in')
