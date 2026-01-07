from django import forms


class SignupForm(forms.Form):
    username = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={
            'placeholder': "Nom d'utilisateur"
        }),
        required=True)

    password = forms.CharField(
        label='',
        widget=forms.PasswordInput(attrs={
            'placeholder': "Mot de passe"
        }),
        required=True)

    confirm_password = forms.CharField(
        label='',
        widget=forms.PasswordInput(attrs={
            'placeholder': "Confirmer mot de passe"
        }),
        required=True)

class LoginForm(forms.Form):
    username = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={
            'placeholder': "Nom d'utilisateur"
        }),
        required=True)

    password = forms.CharField(
        label='',
        widget=forms.PasswordInput(attrs={
            'placeholder': "Mot de passe"
        }),
        required=True)
