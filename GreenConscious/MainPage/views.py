from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from MainPage.models import Event

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
