from django.urls import path
from user.views import Sign_in, Sign_up,logout_view,activate_user,admin_dashboard



urlpatterns = [
    path('signup/', Sign_up, name='signup'),
    path('sign-in/', Sign_in, name='sign-in'),
    path('logout/', logout_view, name='logout'),
    path('activate/<int:user_id>/<str:token>/',activate_user),
    path('admin/dashboard/',admin_dashboard,name='admin_dashboard')


]