from django import forms

class EventCreationForm(forms.Form):
    event_name =forms.CharField(required=True,
                                label='Event Name',
                                widget=forms.TextInput(attrs={'class':'eventName_field',
                                                              'placeholder':'Please enter event name'}))
    event_description =forms.CharField(required=True,
                                       label='Event Description',
                                       widget=forms.Textarea(attrs={'class':'form-control',
                                                                    'placeholder':'Please enter event description'}))
    event_date =forms.DateField(required=True,
                                label='Event Date',
                                widget=forms.SelectDateWidget(attrs={'class':'dateTime_field',}))
    event_time =forms.TimeField(required=True,
                                label='Event Time',
                                widget=forms.TimeInput(format='%H:%M', attrs={'class':'dateTime_field',
                                                                              'type': 'time',
                                                                              'placeholder': 'HH:MM'}))