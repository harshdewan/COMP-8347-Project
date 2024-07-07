from django.urls import path
from . import views

app_name = 'Login_SignUp'

urlpatterns = [
    path('', views.login, name='login'),
    path('login/', views.login,  name='login'),
    path('logout/', views.logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('profile/<str:inputUserName>/', views.profile_view, name='profile_view'),
    path('change_password/<str:inputUserName>/', views.change_password_view, name='change_password'),
    path('change_profile_image/<str:inputUserName>/', views.change_profile_image_view, name='change_profile_image'),
    path('main_page/', views.main_page_view, name='main_page'),

]
