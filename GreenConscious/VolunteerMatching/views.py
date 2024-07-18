# views.py in VolunteerMatching app

from django.shortcuts import render

from Login_SignUp.models import UserProfile
from .forms import VolunteerMatchingForm
from MainPage.models import Event, EventCategory


def volunteer_matching(request):
    matched_events = None
    if request.method == 'POST':
        form = VolunteerMatchingForm(request.POST)
        if form.is_valid():
            interest = form.cleaned_data['userEventInterested']
            date = form.cleaned_data['date']
            matched_events = Event.objects.filter(start_date__gte=date, category=interest)
            print("matched events: ", matched_events)
    else:
        form = VolunteerMatchingForm()
    return render(request, 'VolunteerMatching/volunteer_matching.html', {'form': form, 'matched_events': matched_events})
