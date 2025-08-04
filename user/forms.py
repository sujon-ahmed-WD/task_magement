import re
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User,Group,Permission
from tasks.forms import StyledFormMixin
from django.contrib.auth.forms import AuthenticationForm,PasswordChangeForm,PasswordResetForm,SetPasswordForm

from django import forms

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs) # super mna halo override

        for fieldname in ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

class CustomRegisterForm(StyledFormMixin, forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput)
    conform_password = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'conform_password']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_styled_widgets()
        
    def clean_password1(self): # field Error 
        password1 = self.cleaned_data.get('password1')
        errors=[]
        
        if len(password1) < 8:
            errors.append("Password must be at least 8 characters long.")
        if not re.search(r'[A-Z]', password1):
            errors.append("Password must contain at least one uppercase letter.")
        if not re.search(r'[a-z]', password1):
            errors.append("Password must contain at least one lowercase letter.")   
        if not re.search(r'[0-9]', password1):
            errors.append("Password must contain at least one digit.")
        if  "abc" in password1:
            errors.append("Password cannot contain the substring 'abc'.")
        
        if  errors:
            raise forms.ValidationError(errors)
        return password1
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        email_exists=User.objects.filter(email=email).exists()
        
        if email_exists:
            raise forms.ValidationError("Email already exists")
    
        return email
    
    
    def clean(self): # not field Error
         cleaned_data = super().clean()
         password1 = cleaned_data.get('password1')
         conform_password = cleaned_data.get('conform_password')

         if password1 and conform_password and password1 != conform_password:
             raise forms.ValidationError("Password and conform password are not same")
         
        
class LoginForm(StyledFormMixin,AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_styled_widgets()
   
class AssignRoleForm(StyledFormMixin,forms.Form):
    role = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        empty_label="Select a Role"
    )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_styled_widgets()
        

class CreateGroupForm(StyledFormMixin, forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='Assign Permission'
    )
    
    class Meta:
        model = Group
        fields = ['name', 'permissions']


class CustomPasswordChangeForm(StyledFormMixin,PasswordChangeForm):
    pass
class CustomPasswordResetForm(StyledFormMixin,PasswordResetForm):
    pass


class CustomPasswordResetConfirmForm(StyledFormMixin,PasswordResetForm):
    pass

