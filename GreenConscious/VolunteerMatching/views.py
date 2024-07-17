# views.py in VolunteerMatching app

from django.shortcuts import render

from Login_SignUp.models import UserProfile
from .forms import VolunteerMatchingForm
from MainPage.models import Event, EventCategory


def volunteer_matching(request):
    #interest = EventCategory.objects.all()
    #print(interest)
    matched_events = None
    if request.method == 'POST':
        form = VolunteerMatchingForm(request.POST, user=request.user)
        if form.is_valid():
            interest = form.cleaned_data['interest']
            date = form.cleaned_data['date']
            matched_events = Event.objects.filter(start_date=date, category=interest)
    else:
        form = VolunteerMatchingForm(user=request.user)

    #print("---> ", request.user.username)
    print("---> ", UserProfile.objects.get(user=request.user).eventInterested)
    return render(request, 'VolunteerMatching/volunteer_matching.html', {'form': form, 'matched_events': matched_events})
