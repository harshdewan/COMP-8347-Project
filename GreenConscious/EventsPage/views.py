from django.shortcuts import render, redirect

from .forms import EventCreationForm, EventRegistrationForm
from django.http import HttpResponse
from MainPage.models import Event
from .models import EventRegistration


# Create your views here.
def event_creation(request):
    if request.method == 'POST':
        form = EventCreationForm(request.POST)
        if form.is_valid():
            event_name = form.cleaned_data['event_name']
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            event_description = form.cleaned_data['event_description']

            e = Event(name=event_name,
                      start_date=start_date,
                      end_date=end_date,
                      description=event_description,
                      created_by=request.user)
            e.save()

            return redirect(to='MainPage:main_page')
        else:
            return HttpResponse('Invalid Data')
    return render(request, 'event_creation.html', {'form': EventCreationForm})


def event_registration(request, event_id):
    if request.method == 'POST':
        form = EventRegistrationForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone_no']

            er = EventRegistration(eventId=event_id,
                                   user_id=request.user,
                                   name=name,
                                   email=email,
                                   phone_number=phone)
            er.save()

            return redirect(to='MainPage:main_page')
        else:
            print(form.errors)
            return HttpResponse('Invalid Data')
    return render(request, 'event_registration.html', {'form': EventRegistrationForm,
                                                       'event_id': event_id})
