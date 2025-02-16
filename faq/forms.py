from django import forms
from .models import Faq


class FaqForm(forms.ModelForm):
    class Meta:
        model = Faq
        fields = ('question',)

    question = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 5,
            'cols': 50,
            'class':
            'form-control'}),
        help_text="Maximum length is 255 characters."
    )
