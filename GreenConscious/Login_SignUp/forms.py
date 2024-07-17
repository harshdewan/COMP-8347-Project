#LoginForm
#SignUp Form
#Profile

from django import forms

from django.contrib.auth.models import User


class signupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), label='Password', max_length=10)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        help_texts = {
            'username': None,
        }
        labels = {
            'username': 'Username',
            'email': 'Email',
            'password': 'Password'
        }


class loginForm(forms.Form):
    loginUserName = forms.CharField(max_length=50, label="Username")
    loginPassword = forms.CharField(widget=forms.PasswordInput(), label="Password")


class profileForm(forms.Form):
    userFirstName = forms.CharField(max_length=50, label="First Name")
    userLastName = forms.CharField(max_length=50, label="Last Name")
    userCity = forms.CharField(max_length=50, label="City")
    userCountry = forms.CharField(max_length=50, label="Country")


class PasswordChangeForm(forms.Form):
    oldPassword = forms.CharField(widget=forms.PasswordInput(attrs={'class' : 'input-group'}), label="Old Password")
    newPassword = forms.CharField(widget=forms.PasswordInput(attrs={'class' : 'input-group'}), label="New Password")
    confirmPassword = forms.CharField(widget=forms.PasswordInput(attrs={'class' : 'input-group'}), label="Confirm Password")
