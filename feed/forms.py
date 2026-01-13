from django import forms
from feed.models import Ticket, Review


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
