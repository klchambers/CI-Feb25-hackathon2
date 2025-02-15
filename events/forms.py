from django import forms
from .models import Event

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'category', 'date', 'duration', 
                  'location_name', 'address', 'city', 'state', 'zip_code', 
                  'price', 'capacity', 'image']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ensure image is optional
        self.fields['image'].required = False
