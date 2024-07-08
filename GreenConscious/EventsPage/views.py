from django.shortcuts import render

from .forms import EventCreationForm
from django.http import HttpResponse
from MainPage.models import Event

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
            return render(request, template_name='MainPage/main_page.html', context={'event': e})
        else:
            return HttpResponse('Invalid Data')
    return render(request, 'event_creation.html', {'form': EventCreationForm})
