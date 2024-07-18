from django.http import HttpResponse
from django.shortcuts import render, redirect
from Login_SignUp.forms import signupForm, loginForm, profileForm, PasswordChangeForm, ResetPasswordForm, \
    SecurityQuestionForm, ResetPasswordNextForm
from Login_SignUp.models import UserProfile, SecurityAnswer, SecurityQuestion
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
import random


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
                    return HttpResponse('Invalid Username/Password, Please try again')
            except User.DoesNotExist:
                return HttpResponse('Invalid Username/Password, Please try again')
        else:
            return HttpResponse('Invalid Data !')
    else:
        form = loginForm()
        return render(request, template_name='login.html', context={'form': form})


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
                return redirect('Login_SignUp:add_security_questions', user_id=user.id)
            except Exception as exception:
                return HttpResponse(f'Signup failed: {exception}')
        else:
            return HttpResponse('Invalid Data !!')
    else:
        form = signupForm()
        return render(request, template_name='signup.html', context={'form': form})


def profile(request):
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
                try:
                    userProfile = UserProfile.objects.get(user=userDetails)
                except Exception:
                    userProfile = None

                if userProfile is None:
                    userProfile = UserProfile.objects.create(user=userDetails,
                                                             city=userCity, country=userCountry,
                                                             profileImage='')
                    userDetails.save()
                    userProfile.save()
                else:
                    userDetails.save()
                    userProfile = (UserProfile.objects.filter(user=userDetails).update(city=userCity, country=userCountry,
                                                         profileImage=''))

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
                    'userCountry': ""
                }
                form = profileForm(initial=initial_data)
            else:
                print("firstname: ", userprofile_details.user.first_name)
                print("lastname: ", userprofile_details.user.last_name)
                initial_data = {
                    'userFirstName': userprofile_details.user.first_name,
                    'userLastName': userprofile_details.user.last_name,
                    'userCity': userprofile_details.city,
                    'userCountry': userprofile_details.country,
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
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['userName']
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return HttpResponse('Incorrect username, Please try again')

            # Redirect to a new page for step 2
            return redirect('Login_SignUp:passwordresetnext', user_id=user.id)
        else:
            return HttpResponse('Invalid Data, Please try again')
    else:
        form = ResetPasswordForm()
        return render(request, template_name='passwordreset.html', context={'form': form})


def password_reset_next(request, user_id):
    if request.method == 'POST':
        form = ResetPasswordNextForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['userName']
            question_id = form.cleaned_data['question_id']
            answer = form.cleaned_data['answer']

            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return HttpResponse('Incorrect username, Please try again')

            try:
                security_answer = SecurityAnswer.objects.get(user=user, question_id=question_id)
                if security_answer.answer == answer:
                    # Perform password reset logic here
                    # Example: For demonstration, assuming a successful password reset
                    # In real implementation, you would implement your own password reset mechanism
                    # For example, using Django's built-in password reset functionality
                    user.set_password(form.cleaned_data['newPassword'])
                    user.save()
                    return redirect('Login_SignUp:loginPage')
                else:
                    return HttpResponse('Incorrect answer, Please try again')
            except SecurityAnswer.DoesNotExist:
                return HttpResponse('Security answer not found, Please try again')

        else:
            return HttpResponse('Invalid Data, Please try again')
    else:
        form = ResetPasswordNextForm()
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return HttpResponse('Incorrect user ID, Please try again')

        user_questions = SecurityAnswer.objects.filter(user=user).select_related('question')

        if not user_questions.exists():
            return HttpResponse('No security answers found, Please try again')

        security_question = random.choice(user_questions)
        print("security_question", security_question)

        return render(request, 'passwordresetnext.html', {
            'form': form,
            'user_id': user_id,
            'security_question': security_question,
        })

def add_security_questions(request, user_id):
    user = User.objects.get(id=user_id)
    if request.method == 'POST':
        form = SecurityQuestionForm(request.POST)
        if form.is_valid():
            question1 = form.cleaned_data['question1']
            answer1 = form.cleaned_data['answer1']
            question2 = form.cleaned_data['question2']
            answer2 = form.cleaned_data['answer2']
            question3 = form.cleaned_data['question3']
            answer3 = form.cleaned_data['answer3']

            SecurityAnswer.objects.create(user=user, question=question1, answer=answer1)
            SecurityAnswer.objects.create(user=user, question=question2, answer=answer2)
            SecurityAnswer.objects.create(user=user, question=question3, answer=answer3)

            return redirect('Login_SignUp:loginPage')
    else:
        form = SecurityQuestionForm()
    return render(request, template_name='add_security_questions.html', context={'form': form})
