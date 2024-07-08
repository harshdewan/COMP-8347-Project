from django.urls import path
from . import views

app_name = 'EventsPage'

urlpatterns = [
    path('', views.event_creation, name='event_creation'),
    path('event_creation', views.event_creation, name='event_creation'),
]