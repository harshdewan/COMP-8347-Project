from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

from Login_SignUp.forms import signupForm, loginForm, profileForm
from Login_SignUp.models import UserProfile
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login


def loginPage(request):
    if request.method == 'POST':
        print("post section login")
        form = loginForm(request.POST)
        if form.is_valid():
            userName = form.cleaned_data['loginUserName']
            userPassword = form.cleaned_data['loginPassword']
            print("userName: ", userName,  " userPassword: ", userPassword)
            try:
                checkUserName = User.objects.get(username=userName)
                user = authenticate(request, username=userName, password=userPassword)
                if user is not None:
                    login(request, user)
                    print("after login function")
                    return redirect('MainPage:main_page')
                else:
                    return HttpResponse('Unable to login, Please try again')
            except User.DoesNotExist:
                return HttpResponse('Invalid Username/Password, Please try again')
        else:
            return HttpResponse('Invalid Data')
    else:
        form = loginForm()
        return render(request, template_name='login.html', context={'form': form})


def logoutPage(request):
    if request.user.is_authenticated:
        return render(request, template_name='logout.html', context={})
    else:
        return redirect('Login_SignUp:homePage')


def signupPage(request):
    if request.method == 'POST':
        form = signupForm(request.POST)
        if form.is_valid():
            userName = form.cleaned_data['username']
            userEmail = form.cleaned_data['email']
            userPassword = form.cleaned_data['password']
            user = User.objects.create(username=userName, email=userEmail, password=userPassword)
            try:
                user.save()
            except Exception as exception:
                return HttpResponse(f'Signup failed: {exception}')
            return render(request, template_name='login.html', context={'form': loginForm})
        else:
            return HttpResponse('Invalid Data')
    else:
        form = signupForm()
        return render(request, template_name='signup.html', context={'form': form})


def profile_view(request):
    if request.user.is_authenticated:
        inputUserName = request.user.username
        print("called received in profile: ", inputUserName)
        userDetails = User.objects.get(username=inputUserName)
        if request.method == 'POST':
            form = profileForm(request.POST)
            if form.is_valid():
                userFirstName = form.cleaned_data['userFirstName']
                userLastName = form.cleaned_data['userLastName']
                userCity = form.cleaned_data['userCity']
                userCountry = form.cleaned_data['userCountry']
                userDetails.first_name = userFirstName
                userDetails.last_name  = userLastName
                userProfile = UserProfile.objects.create(user=userDetails,
                                            city=userCity, country=userCountry,
                                                         profileImage='')
                userProfile.save()
                return redirect('MainPage:main_page')
        else:
            initial_data = {
                'userFirstName': "",
                'userLastName': "",
                'userCity': "",
                'userCountry': ""
            }
            form = profileForm(initial=initial_data)
            context = {
                'form': form,
                'userDetails': userDetails,
            }
            return render(request, 'profile.html', context)
    else:
        return render(request, template_name='homepage.html', context={})


def change_password_view(request, inputUserName):
    # Handle password change logic here
    return HttpResponse("Change Password Page")  # Replace with your logic


def change_profile_image_view(request, inputUserName):
    # Handle profile image change logic here
    return HttpResponse("Change Profile Image Page")  # Replace with your logic


def homePage(request):
    return render(request, template_name='homepage.html', context={})
