from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

from Login_SignUp.forms import signupForm, loginForm, profileForm
from Login_SignUp.models import UserProfileDetails, UserLoginCredentials


def login(request):
    if request.method == 'POST':
        form = loginForm(request.POST)
        if form.is_valid():
            userName = form.cleaned_data['loginUserName']
            userPassword = form.cleaned_data['loginPassword']
            try:
                checkUserName = UserLoginCredentials.objects.get(userName=userName)
            except UserLoginCredentials.DoesNotExist:
                return HttpResponse('Invalid Username, Please try again')

            if userPassword != checkUserName.userPassword:
                return HttpResponse('Invalid Password, Please try again')

            #return render(request, template_name='login.html', context={'form': form})
            return redirect('Login_SignUp:profile_view', inputUserName=userName)
        else:
            return HttpResponse('Invalid Data')
    else:
        form = loginForm()
        return render(request, template_name='login.html', context={'form': form})


def logout(request):
    if request.method == 'POST':
        # Perform logout actions if needed
        return render(request, template_name='logout.html', context={})
    else:
        return render(request, template_name='logout.html', context={})


def signup(request):
    if request.method == 'POST':
        form = signupForm(request.POST)
        if form.is_valid():
            userName = form.cleaned_data['userName']
            userEmail = form.cleaned_data['userEmail']
            userPassword = form.cleaned_data['userPassword']
            user = UserLoginCredentials(userName=userName, userEmail=userEmail, userPassword=userPassword)
            try:
                user.save()
            except Exception as e:
                return HttpResponse(f'Signup failed: {e}')

            return render(request, template_name='login.html', context={'form': loginForm})
        else:
            return HttpResponse('Invalid Data')
    else:
        form = signupForm()
        return render(request, template_name='signup.html', context={'form': form})


def profile_view_old(request, inputUserName):
    if request.method == 'POST':
        form = profileForm(request.POST)
        if form.is_valid():
            userFirstName = form.cleaned_data['userFirstName']
            userLastName = form.cleaned_data['userLastName']
            userCity = form.cleaned_data['userCity']
            userCountry = form.cleaned_data['userCountry']
            userProfile = UserProfileDetails(userName=UserLoginCredentials.get(userName=inputUserName), userFirstName=userFirstName, userLastName =userLastName, userCity = userCity, userCountry = userCountry)
            try:
                userProfile.save()
            except Exception as e:
                return HttpResponse(f'User profile save failed: {e}')
            return render(request, template_name='login.html', context={'form': loginForm}) ##redirect to main page
        else:
            return HttpResponse('Invalid Data')
    else:
        form = profileForm()
        userDetails = UserLoginCredentials.get(userName=inputUserName)
        form['userName'] = userDetails.userName
        form['userEmail'] = userDetails.userEmail
        form['userPassword'] = userDetails.userPassword
        return render(request, 'profile.html', {'form': form})


def profile_view(request, inputUserName):
    print("called received in profile: ", inputUserName)
    userDetailsList = UserLoginCredentials.objects.all()
    for user in userDetailsList:
        print("user: ", user.__str__())
    userDetails = UserLoginCredentials.objects.get(userName=inputUserName)
    if request.method == 'POST':
        form = profileForm(request.POST)
        if form.is_valid():
            userFirstName = form.cleaned_data['userFirstName']
            userLastName = form.cleaned_data['userLastName']
            userCity = form.cleaned_data['userCity']
            userCountry = form.cleaned_data['userCountry']

            userProfile = UserProfileDetails.objects.create(
                userName=userDetails,
                firstName=userFirstName,
                lastName=userLastName,
                city=userCity,
                country=userCountry
            )
            return redirect('Login_SignUp:main_page')
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


def change_password_view(request, inputUserName):
    # Handle password change logic here
    return HttpResponse("Change Password Page")  # Replace with your logic


def change_profile_image_view(request, inputUserName):
    # Handle profile image change logic here
    return HttpResponse("Change Profile Image Page")  # Replace with your logic


def main_page_view(request):
    return HttpResponse("Main Page")  # Replace with your main page logic