from django.http import HttpResponse
from django.shortcuts import redirect, render

from django.contrib.auth.models import User, Group
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required,user_passes_test

# import user
from user.forms import CustomRegisterForm, AssignRoleForm, CreateGroupForm
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator

from user.forms import LoginForm



# Create your views here.
# Test in users

def is_admin(user):
    return user.groups.filter(name='admin').exists()


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


def Sign_in(request):
    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home")
    return render(request, "registration/login.html", {"form": form})

@login_required
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
            return redirect("sign-in")
        else:
            print("Invalid token")
            return HttpResponse("Invalid Id or token")
    except User.DoesNotExist:
        print("User not found")
        return HttpResponse("User not found")

@user_passes_test(is_admin,login_url='no-permission')
def admin_dashboard(request):
    users = User.objects.all()
    return render(request, "admin/dashboard.html", {"users": users})

@user_passes_test(is_admin,login_url='no-permission')
def assign_role(request, user_id):
    user = User.objects.get(id=user_id)
    form = AssignRoleForm()

    if request.method == "POST":
        form = AssignRoleForm(request.POST)
        if form.is_valid():
            role = form.cleaned_data.get("role")
            user.groups.clear()
            user.groups.add(role)
            messages.success(
                request,
                f"User{user.username} has been assigned to the {role.name} role",
            )
            return redirect("admin-dashboard")
    return render(request, "admin/assign_role.html", {"form": form})

@user_passes_test(is_admin,login_url='no-permission')

def create_group(request):
    form = CreateGroupForm()
    if request.method == "POST":
        form = CreateGroupForm(request.POST)  # confusion

        if form.is_valid():
            group = form.save()
            messages.success(
                request, f"User{group.username} has been created successfully"
            )
            return redirect("create-group")
    return render(request, "admin/create_group.html", {"form": form})

@user_passes_test(is_admin,login_url='no-permission')
def group_list(request):
    groups = Group.objects.all()
    return render(request, "admin/groups_list.html", {"groups": groups})
