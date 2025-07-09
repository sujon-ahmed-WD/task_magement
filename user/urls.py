from django.urls import path
from user.views import Sign_up



urlpatterns = [
    path('signup/', Sign_up, name='signup'),
     
    
]