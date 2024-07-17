from django.urls import path
from . import views

app_name = 'MainPage'

urlpatterns = [
    path('home/', views.main_page, name='main_page'),
    path('event/<int:event_id>/', views.event_detail, name='event_detail'),
    path('past_events/', views.past_events, name='past_events'),  # Add this line
]
