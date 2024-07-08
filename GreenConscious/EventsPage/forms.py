from django import forms


class EventCreationForm(forms.Form):
    event_name = forms.CharField(required=True,
                                 label='Event Name',
                                 widget=forms.TextInput(attrs={'class': 'input_field',
                                                               'placeholder': 'Please enter event name'}))
    event_description = forms.CharField(required=True,
                                        label='Event Description',
                                        widget=forms.Textarea(attrs={'class': 'form-control',
                                                                     'placeholder': 'Please enter event description'}))
    start_date = forms.DateField(required=True,
                                 label='Event Start Date',
                                 widget=forms.SelectDateWidget(attrs={'class': 'dateTime_field'}))
    end_date = forms.DateField(required=True,
                               label='Event End Date',
                               widget=forms.SelectDateWidget(attrs={'class': 'dateTime_field', }))
    event_time = forms.TimeField(required=True,
                                 label='Event Time',
                                 widget=forms.TimeInput(format='%H:%M', attrs={'class': 'dateTime_field',
                                                                               'type': 'time',
                                                                               'placeholder': 'HH:MM'}))


class EventRegistrationForm(forms.Form):
    name = forms.CharField(required=True,
                           label='Name',
                           widget=forms.TextInput(attrs={'class': 'input_field',
                                                         'placeholder': 'Please enter your name'}))
    email = forms.EmailField(required=True,
                             label='Email',
                             widget=forms.TextInput(attrs={'class': 'input_field',
                                                           'placeholder': 'Please enter your email'}))
    phone_no = forms.CharField(required=True,
                               label='Phone Number',
                               widget=forms.TextInput(attrs={'class': 'input_field',
                                                             'placeholder': 'Please enter your phone no.'}))
