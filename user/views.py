from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
import user
from user.forms import CustomRegisterForm, RegisterForm
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator

from user.forms import LoginForm


# Create your views here.
def Sign_up(request):
    if request.method == "POST":
        form = CustomRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            print("user", user)
            user.set_password(form.cleaned_data.get("password1"))
            print(form.cleaned_data)
            user.is_active = False
            user.save()
            messages.success(
                request, "A confirmation mail has been sent. Please check your email."
            )
            
            return redirect("sign-in")
        else:
            print("FORM is not valid")
    else:
        form = CustomRegisterForm()

    return render(request, "registration/register.html", {"form": form})


# def Sign_in(request):

#     if request.method == "POST":
#         username = request.POST.get("username")
#         password = request.POST.get("password")

#         user = authenticate(username=username, password=password)
#         print(user)


#         if user is not None:
#             login(request, user)
#             print(user.username)
#             return redirect("home")
#     return render(request, "registration/login.html")
def Sign_in(request):
    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home")
    return render(request, "registration/login.html",{"form":form})


def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect("sign-in")


def activate_user(request, user_id, token):
    try:
        print(f"Received user_id={user_id}, token={token}")
        user = User.objects.get(id=user_id)
        if default_token_generator.check_token(user, token):
            print("Token valid. Activating user...")
            user.is_active = True
            user.save()
            return redirect('sign-in')
        else:
            print("Invalid token")
            return HttpResponse('Invalid Id or token')
    except User.DoesNotExist:
        print("User not found")
        return HttpResponse('User not found')

def admin_dashboard(request):
    return render(request,'admin/dashboard.html')