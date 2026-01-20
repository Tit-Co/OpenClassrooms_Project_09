from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from feed.models import Ticket, Review, UserFollows


User = get_user_model()


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ["title", "description", "image"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-input"}),
            "description": forms.Textarea(attrs={"class": "form-textarea"}),
            "image": forms.ClearableFileInput(attrs={
                "class": "file-input",
                "id": "image-upload"
            }),
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["headline", "rating", "body"]
        widgets = {
            "headline": forms.TextInput(attrs={"class": "form-input"}),
            "body": forms.Textarea(attrs={"class": "form-textarea"}),
            "rating": forms.RadioSelect(choices=[(i, i) for i in range(6)], attrs={"class": "form-radio"}),
        }

class FollowUsersForm(forms.Form):
    username = forms.CharField(max_length=20, label="",
        widget=forms.TextInput(attrs={
            "placeholder": "Nom d'utilisateur",
            "class": "form-input",
        }),
        required=True,
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super().__init__(*args, **kwargs)

    def clean_username(self):
        username = self.cleaned_data["username"]

        try:
            followed_user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise ValidationError("Cet utilisateur n'existe pas.")

        if followed_user == self.user:
            raise ValidationError("Vous ne pouvez pas vous suivre vous-même.")

        if UserFollows.objects.filter(user=self.user, followed_user=followed_user).exists():
            raise ValidationError("Vous suivez déjà cet utilisateur.")

        self.followed_user = followed_user

        return username
