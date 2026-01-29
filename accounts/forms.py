from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password

User = get_user_model()


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username",)

    error_message = {
        "password_too_short": "Le mot de passe doit contenir au moins 8 caractères.",
        "password_too_common": "Ce mot de passe est trop courant.",
        "password_entirely_numeric": "Le mot de passe ne peut pas être uniquement numérique.",
        "password_too_similar": "Le mot de passe est trop proche de votre nom d’utilisateur.",
    }

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

    def clean_username(self):
        """
        Method that checks if the username is already taken.
        Returns:
            The validated username.
        """
        username = self.cleaned_data["username"].lower()
        if User.objects.filter(username=username).exists():
            raise ValidationError("Ce nom d'utilisateur existe déjà.")
        return username

    def clean_password1(self):
        """
        Method that checks if the password is correct.
        Returns:
            The validated password.
        """
        password = self.cleaned_data.get("password1")

        try:
            validate_password(password, self.instance)
        except ValidationError as e:
            raise ValidationError([self.error_message[error.code] for error in e.error_list])
        return password

    def clean_password2(self):
        """
        Method that checks if the password 2 equals the password 1.
        """
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 != password2:
            raise ValidationError("Les mots de passe doivent être identiques.")


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
