from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import USER
from django.contrib.auth import authenticate ,login,logout
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

def Sign_in(request):
     if request.method == "POST":
          username=request.POST.get("username")
          password=request.POST.get("password")
          
          user=authenticate(username=username, password=password)
          print(user)
          
          if user is not None:
               login(request,user)
               print(user.username)
               return  redirect('home')
     return render(request, 'registration/login.html')


def logout_view(request):
     if request.method == "POST":
          logout(request)
          return redirect('sign-in')
     