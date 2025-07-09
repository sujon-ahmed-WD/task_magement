from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import USER
import user
from user.forms import CustomRegisterForm, RegisterForm

# Create your views here.
def Sign_up(request):
    if request.method == "GET":
         form = CustomRegisterForm()
    if request.method == "POST":
         form = CustomRegisterForm(request.POST)
         if form.is_valid():
          #     username=form.cleaned_data.get('username')
          #     password=form.cleaned_data.get('password1')
          #     conform_password=form.cleaned_data.get('password2')
              
          #     if password== conform_password:
          #          user.objects.create(username=username, password=password)
          #     else:
          #          print("Password and conform password are not same")
          form.save()
        

    return render(request, 'registration/register.html', {'form': form})
