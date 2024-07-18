# forms.py in VolunteerMatching app

from django import forms
from Login_SignUp.models import UserProfile
from MainPage.models import Event, EventCategory


class VolunteerMatchingForm(forms.Form):
    userEventInterested = forms.ModelChoiceField(
        queryset=EventCategory.objects.all(),
        label='Select Interest',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
