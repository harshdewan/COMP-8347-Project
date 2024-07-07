#LoginForm
#SignUp Form
#Profile

from django import forms

from Login_SignUp.models import UserLoginCredentials


#from models import UserProfileDetails, UserLoginCredentials


class signupForm(forms.ModelForm):
    userPassword = forms.CharField(widget=forms.PasswordInput(), label= 'Password', max_length=10)
    class Meta:
        model = UserLoginCredentials
        fields = ['userName', 'userEmail', 'userPassword']
        labels = {
            'userName' : 'Username',
            'userEmail' : 'Email',
            'userPassword' : 'Password'
        }


class loginForm(forms.Form):
    loginUserName = forms.CharField(max_length=50, label="Username")
    loginPassword = forms.CharField(widget=forms.PasswordInput(), label="Password")


class profileForm(forms.Form):
    userFirstName = forms.CharField(max_length=50, label="First Name")
    userLastName = forms.CharField(max_length=50, label="Last Name")
    userCity = forms.CharField(max_length=50, label="City")
    userCountry = forms.CharField(max_length=50, label="Country")


