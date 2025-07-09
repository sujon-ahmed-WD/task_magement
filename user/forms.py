import re
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django import forms

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs) # super mna holo overrinde

        for fieldname in ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

class CustomRegisterForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput)
    conform_password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'conform_password']
        
        if len(password1) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long.")
        elif re.fullmatch(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$', password1):
            raise forms.ValidationError("Password must contain at least one letter and one number.")
