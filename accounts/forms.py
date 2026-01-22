from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import get_user_model


User = get_user_model()

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["username"].widget.attrs.update({
            "placeholder": "Nom d'utilisateur",
            "class": "form-input",
        })

        self.fields["password1"].widget.attrs.update({
            "placeholder": "Mot de passe",
            "class": "form-input",
        })

        self.fields["password2"].widget.attrs.update({
            "placeholder": "Confirmer mot de passe",
            "class": "form-input",
        })

        for field in self.fields.values():
            field.label = ""

class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ("username",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["username"].widget.attrs.update({
            "placeholder": "Nom d'utilisateur",
            "class": "form-input",
        })

        self.fields["password"].widget.attrs.update({
            "placeholder": "Mot de passe",
            "class": "form-input",
        })

        for field in self.fields.values():
            field.label = ""
