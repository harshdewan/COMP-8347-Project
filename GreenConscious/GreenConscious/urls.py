"""
URL configuration for GreenConscious project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

# Define URL patterns for each app
greenconscious_patterns = [
    path('', include('Login_SignUp.urls')),
    path('', include('MainPage.urls')),
    path('events/', include('EventsPage.urls')),
    path('community/', include('community.urls')),
    path('volunteer_matching/', include('VolunteerMatching.urls')),
    path('about/', include('About.urls')),
    path('contact/', include('Contact.urls')),
    path('', include('userhistory.urls')),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('greenconscious/', include(greenconscious_patterns)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
