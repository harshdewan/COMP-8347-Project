# forms.py in VolunteerMatching app

from django import forms
from Login_SignUp.models import UserProfile
from MainPage.models import Event, EventCategory


class VolunteerMatchingForm(forms.Form):
    interest = forms.ModelChoiceField(
        queryset=EventCategory.objects.all(),
        label='Select Interest',
        required=True
    )
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(VolunteerMatchingForm, self).__init__(*args, **kwargs)
        if user:
            try:
                user_profile = UserProfile.objects.get(user=user)
                print(user_profile, "  ->  ", user_profile.eventInterested)
                self.fields['interest'].queryset = EventCategory.objects.filter(id=user_profile.eventInterested.id)
            except UserProfile.DoesNotExist:
                self.fields['interest'].queryset = EventCategory.objects.none()
