from django.contrib.auth.models import User
from django.utils import timezone

from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from MainPage.models import Event
from .forms import EventCreationForm
from django.http import HttpResponse

def main_page(request):
    events_list = Event.objects.all()

    # Paginator settings
    paginator = Paginator(events_list, 5)  # Show 10 events per page

    page = request.GET.get('page')
    try:
        events = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        events = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        events = paginator.page(paginator.num_pages)

    return render(request, 'MainPage/main_page.html', {'events': events})


def event_detail(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    return render(request, 'MainPage/event_detail.html', {'event': event})


def past_events(request):
    events_list = Event.objects.filter(end_date__lt=timezone.now()).order_by('-end_date')

    # Paginator settings
    paginator = Paginator(events_list, 5)  # Show 5 events per page

    page = request.GET.get('page')
    try:
        events = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        events = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        events = paginator.page(paginator.num_pages)

    return render(request, 'MainPage/past_events.html', {'events': events})


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
    return render(request, 'Events/event_creation.html', {'form': EventCreationForm})