from django.http import HttpResponse
from django.shortcuts import render, redirect
from Login_SignUp.forms import signupForm, loginForm, profileForm, PasswordChangeForm, ResetPasswordForm
from Login_SignUp.models import UserProfile
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from MainPage.models import EventCategory


def loginPage(request):
    if request.method == 'POST':
        print("post section login")
        form = loginForm(request.POST)
        if form.is_valid():
            userName = form.cleaned_data['loginUserName']
            userPassword = form.cleaned_data['loginPassword']
            print("userName: ", userName, " userPassword: ", userPassword)
            try:
                checkUserName = User.objects.get(username=userName)
                user = authenticate(request, username=userName, password=userPassword)
                if user is not None:
                    login(request, user)
                    print("after login function")
                    return redirect('MainPage:main_page')
                else:
                    return render(request, template_name='login.html', context={'form': form,
                                                                                'invalidMessage': 'Invalid Username/Password. Please try again'})
            except User.DoesNotExist:
                return render(request, template_name='login.html', context={'form': form, 'invalidMessage': 'Invalid Username/Password. Please try again'})

        else:
            return render(request, template_name='login.html', context={'form': form, 'invalidMessage': 'Unable to proceed. Please try again!'})
    else:
        form = loginForm()
        return render(request, template_name='login.html', context={'form': form, 'invalidMessage': ''})


def logoutPage(request):
    if request.user.is_authenticated:
        logout(request)
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
            try:
                user = User.objects.create(username=userName, email=userEmail)
                user.set_password(userPassword)
                user.save()
            except Exception as exception:
                return HttpResponse(f'Signup failed: {exception}')
            return render(request, template_name='login.html', context={'form': loginForm})
        else:
            return render(request, template_name='signup.html', context={'form': form, 'invalidMessage':'Unable to proceed. Please try again'})
    else:
        form = signupForm()
        return render(request, template_name='signup.html', context={'form': form})


def profile(request):
    if request.user.is_authenticated:
        inputUserName = request.user.username
        print("called received in profile: ", inputUserName)
        userDetails = User.objects.get(username=inputUserName)
        if request.method == 'POST':
            form = profileForm(request.POST, request.FILES)
            if form.is_valid():
                userFirstName = form.cleaned_data['userFirstName']
                userLastName = form.cleaned_data['userLastName']
                userCity = form.cleaned_data['userCity']
                userCountry = form.cleaned_data['userCountry']
                userEventInterested = form.cleaned_data['userEventInterested']
                userProfileImage = form.cleaned_data.get('userProfileImage')
                userDetails.first_name = userFirstName
                userDetails.last_name = userLastName
                try:
                    userProfile = UserProfile.objects.get(user=userDetails)
                except Exception:
                    userProfile = None

                if userProfile is None:
                    print("user: userEventInterested: ", userEventInterested)
                    eventCategory = EventCategory.objects.get(name=userEventInterested)
                    print("eventCategoryobject: ", eventCategory.__str__())
                    print("new userProfileImage: ", userProfileImage)
                    userProfile = UserProfile.objects.create(user=userDetails,
                                                             city=userCity, country=userCountry,
                                                             profileImage=userProfileImage, eventInterested=eventCategory)
                    userDetails.save()
                    userProfile.save()
                else:
                    eventCategory = EventCategory.objects.get(name=userEventInterested)
                    print("eventCategoryobject: ", eventCategory.__str__())
                    print("update userProfileImage: ", userProfileImage)
                    userDetails.save()
                    userProfile = (
                        UserProfile.objects.filter(user=userDetails).update(city=userCity, country=userCountry,
                                                                            profileImage=userProfileImage, eventInterested=eventCategory))

                return redirect('MainPage:main_page')
        else:
            try:
                userprofile_details = UserProfile.objects.get(user=userDetails)
            except UserProfile.DoesNotExist:
                userprofile_details = None

            if userprofile_details is None:
                initial_data = {
                    'userFirstName': "",
                    'userLastName': "",
                    'userCity': "",
                    'userCountry': "",
                    'userEventInterested': "",
                    'userProfileImage': "default_profile.png",
                }
                form = profileForm(initial=initial_data)
            else:
                print("firstname: ", userprofile_details.user.first_name)
                print("lastname: ", userprofile_details.user.last_name)
                print("userEventInterestedObject", EventCategory.objects.get(id=userprofile_details.eventInterested.id))
                print("userEventInterestedName", EventCategory.objects.get(id=userprofile_details.eventInterested.id).name)
                initial_data = {
                    'userFirstName': userprofile_details.user.first_name,
                    'userLastName': userprofile_details.user.last_name,
                    'userCity': userprofile_details.city,
                    'userCountry': userprofile_details.country,
                    'userEventInterested': EventCategory.objects.get(id=userprofile_details.eventInterested.id),
                    'userProfileImage': userprofile_details.profileImage
                }
                form = profileForm(initial=initial_data)
            context = {
                'form': form,
                'userDetails': userDetails,
            }
            return render(request, 'profile.html', context)
    else:
        return render(request, template_name='homepage.html', context={})


def change_password(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = PasswordChangeForm(request.POST)
            if form.is_valid():
                oldpassword = form.cleaned_data['oldPassword']
                newpassword = form.cleaned_data['newPassword']
                confirmpassword = form.cleaned_data['confirmPassword']
                user = authenticate(request, username=request.user.username, password=oldpassword)
                if user is not None:
                    if confirmpassword != newpassword:
                        return HttpResponse('Old password and new password did not match, Please try again')
                    else:
                        user.set_password(newpassword)
                        user.save()
                        return render(request, template_name="passwordchangesuccess.html", context={})
                        #return redirect('Login_SignUp:password_change_success')
                else:
                    return HttpResponse('Incorrect old password, Please try again')
            else:
                return HttpResponse('Invalid Data, Please try again')
        else:
            form = PasswordChangeForm()
            return render(request, template_name='changepassword.html', context={'form': form})
    else:
        return redirect('Login_SignUp:homePage')


def change_profile_image_view(request, inputUserName):
    # Handle profile image change logic here
    return HttpResponse("Change Profile Image Page")  # Replace with your logic


def homePage(request):
    return render(request, template_name='homepage.html', context={})


def password_change_success(request):
    if request.user.is_authenticated:
        return render(request, template_name='passwordchangesuccess.html', context={})
    else:
        return redirect('Login_SignUp:homePage')


def password_reset(request):
    if request.method == 'POST':
        print("password reset view if")
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['userName']
            newpassword = form.cleaned_data['newPassword']
            confirmpassword = form.cleaned_data['confirmPassword']
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                user = None
            if user is not None:
                if confirmpassword != newpassword:
                    return HttpResponse('confirm password and new password did not match, Please try again')
                else:
                    user.set_password(newpassword)
                    user.save()
                    return render(request, template_name="passwordchangesuccess.html", context={})
                    # return redirect('Login_SignUp:password_change_success')
            else:
                return HttpResponse('Incorrect username, Please try again')
        else:
            return HttpResponse('Invalid Data, Please try again')
    else:
        print("password reset view else")
        form = ResetPasswordForm()
        return render(request, template_name='passwordreset.html', context={'form': form})
