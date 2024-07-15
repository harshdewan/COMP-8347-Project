from django.urls import path
from . import views

app_name = 'Login_SignUp'

urlpatterns = [
    path('', views.homePage, name='homePage'),
    path('login/', views.loginPage,  name='loginPage'),
    path('logout/', views.logoutPage, name='logoutPage'),
    path('signup/', views.signupPage, name='signupPage'),
    path('profile/<str:inputUserName>/', views.profile_view, name='profile_view'),
    path('change_password/<str:inputUserName>/', views.change_password_view, name='change_password'),
    path('change_profile_image/<str:inputUserName>/', views.change_profile_image_view, name='change_profile_image'),
]
