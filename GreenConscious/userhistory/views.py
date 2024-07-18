import datetime
from django.shortcuts import render


def user_history(request):
    visit_count = request.session.get('visit_count', 0)
    last_visit = request.session.get('last_visit')

    # Update visit count and last visit time
    visit_count += 1
    last_visit_time = datetime.datetime.now()

    # Store last visit time as ISO formatted string in session
    request.session['visit_count'] = visit_count
    request.session['last_visit'] = last_visit_time.isoformat()

    context = {
        'visit_count': visit_count,
        'last_visit': last_visit_time.strftime('%Y-%m-%d %H:%M:%S') if last_visit_time else 'Never'
    }
    return render(request, 'history.html', context)
