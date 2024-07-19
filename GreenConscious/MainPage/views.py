from datetime import datetime

from django.contrib.auth.models import User
from django.utils import timezone

from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from EventsPage.forms import EventCreationForm
from MainPage.models import Event, EventCategory
from django.db.models import Q
from django.http import HttpResponse


def parse_custom_date(date_str):
    try:
        # Attempting to parse the date string in the format "Month. Day, Year"
        return datetime.strptime(date_str, '%b. %d, %Y').date()
    except ValueError:
        return None


def main_page(request):
    if not request.user.is_authenticated:
        return redirect('Login_SignUp:homePage')
    print("inside main_page for view function", "<", request.user.username, ">", "<", request.user.is_authenticated,
          ">")
    query = request.GET.get('q')
    category_id = request.GET.get('category')
    events_list = Event.objects.all()

    # filter events
    if category_id:
        events_list = events_list.filter(category_id=category_id)

    if query:
        # Initially checking if the search input is a date or not
        query_date = parse_custom_date(query)
        if query_date:
            events_list = events_list.filter(Q(start_date=query_date) | Q(end_date=query_date))
        else:
            # If the search input isn't a date, filtering the date with event name
            events_list = events_list.filter(Q(name__icontains=query))

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

    categories = EventCategory.objects.all()  # Retrieve all event categories

    return render(request, 'MainPage/main_page.html', {'events': events,
                                                       'query': query,
                                                       'categories': categories,
                                                       'selected_category': int(category_id) if category_id else None
                                                       })


def event_detail(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    disable_flag = True
    event_creator_user_id = event.created_by.id

    if request.user.id == event_creator_user_id:
        disable_flag = False

    return render(request, 'MainPage/event_detail.html',
                  {'event': event, 'disable_flag': disable_flag})


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


def event_update(request, event_id):
    if not request.user.is_authenticated:
        return redirect('Login_SignUp:homePage')

    event = get_object_or_404(Event, id=event_id)

    if request.method == 'POST':
        form = EventCreationForm(request.POST, request.FILES)
        if form.is_valid():
            event.name = form.cleaned_data['event_name']
            event.start_date = form.cleaned_data['start_date']
            event.end_date = form.cleaned_data['end_date']
            event.description = form.cleaned_data['event_description']
            event.location = form.cleaned_data['location']
            event.category = form.cleaned_data['event_category']
            if 'image-clear' in request.POST:
                event.image.delete()
                event.image = None
            elif 'image' in request.FILES:
                event.image = request.FILES['image']
            event.save()

            return redirect('MainPage:event_detail', event_id=event.id)
        else:
            return render(request, 'MainPage/event_update.html', {'form': form,
                                                                  'given_event_id': event_id})
    else:
        form = EventCreationForm(initial={
            'event_name': event.name,
            'start_date': event.start_date,
            'end_date': event.end_date,
            'event_description': event.description,
            'location': event.location,
            'image': event.image,
            'event_category': event.category,
        })
        return render(request, 'MainPage/event_update.html', {'form': form,
                                                              'given_event_id': event_id})
