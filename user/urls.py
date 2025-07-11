from django.urls import path
from user.views import Sign_in, Sign_up, logout_view



urlpatterns = [
    path('signup/', Sign_up, name='signup'),
    path('sign_in/', Sign_in, name='sign-in'),
    path('logout/', logout_view, name='logout'),


]