from django import forms
from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["bio", "location"]
        widgets = {
            "bio": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "location": forms.TextInput(attrs={"class": "form-control"}),
        }