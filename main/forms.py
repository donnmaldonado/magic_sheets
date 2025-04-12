from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

# UserRegistrationForm is a form that allows users to register for an account
class UserRegistrationForm(UserCreationForm):
    # UserCreationForm already has username and password fields
    # Add a custom field for email
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email'
        })
    )

    class Meta:
        # this tells django which model to use
        model = User    
        # this tells django which fields to include in the form
        fields = ('username', 'email', 'password1', 'password2') 

    # customizing the form to use bootstrap classes
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to all fields
        for field_name in self.fields:
            self.fields[field_name].widget.attrs['class'] = 'form-control'

# UserLoginForm is a form that allows users to login to their account
class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter your username'
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter your password'
        })