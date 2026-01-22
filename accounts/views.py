from django.contrib.auth import login, logout
from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect


from accounts.forms import SignupForm, LoginForm


def log_in(request: HttpRequest) -> HttpResponse:
    """
    Method to login
    Args:
        request (HttpRequest): Http request

    Returns:
        An HttpResponse to the accounts application homepage and whose content is filled with the login form.
    """
    if request.method == 'POST':
        login_form  = LoginForm(request=request, data=request.POST)
        if login_form.is_valid():
            user = login_form.get_user()
            login(request, user)
            messages.success(request, f"✅ {user}, connexion réussie.")
            return redirect('feed:feed')
        else:
            messages.error(request=request, message="❌ Identifiants incorrects.")
    else:
        login_form = LoginForm()

    return render(request=request, template_name='accounts/index.html', context={'login_form': login_form})

def sign_up(request: HttpRequest) -> HttpResponse:
    """
    Method to sign up
    Args:
        request (HttpRequest): Http request

    Returns:
        An HttpResponse to the accounts application signup page and whose content is filled with the signup form.
    """
    if request.method == "POST":
        signup_form = SignupForm(data=request.POST)
        if signup_form.is_valid():
            user = signup_form.save()
            login(request=request, user=user)
            messages.success(request, f"✅ {user}, inscription réussie. Vous êtes maintenant connecté.")
            return redirect('feed:feed')
        else:
            messages.error(request=request, message="❌ L'inscription a échoué. Veuillez réessayer.")
    else:
        signup_form = SignupForm()

    return render(request=request, template_name='accounts/sign_up.html', context={'signup_form': signup_form})

def log_out(request: HttpRequest) -> HttpResponse:
    """
    Method to logout
    Args:
        request (HttpRequest): Http request

    Returns:
        An HttpResponseRedirect to the accounts application login page after logout.
    """
    logout(request=request)
    messages.success(request=request, message="✅ Deconnexion réussie.")
    return redirect(to='log-in')
