from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('main_page/', include('MainPage.urls')),  # Ensure the MainPage URLs are included
    path('users/', include('Login_SignUp.urls')),
    path('events/', include('EventsPage.urls')),
    path('about/', include('About.urls')),  # Specify a unique path for the About app
    path('contact/', include('Contact.urls')),
    path('', include('userhistory.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
