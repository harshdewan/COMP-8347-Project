# userhistory/middleware.py

import datetime


class UserHistoryMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        # Track user visits
        session_key = 'user_history'
        visit_time = datetime.datetime.now()

        if session_key in request.session:
            visit_count, last_visit = request.session[session_key]
            if last_visit.date() == visit_time.date():
                visit_count += 1
            else:
                visit_count = 1
        else:
            visit_count = 1

        request.session[session_key] = (visit_count, visit_time)

        # Optionally, you can log the visit in your database or perform other actions
        # For example, logging the visit in a database:
        # UserVisit.objects.create(user=request.user, visit_time=visit_time)

        return None  # Return None to continue processing the request
