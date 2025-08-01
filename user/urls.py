from django.urls import path
from user.views import Sign_in, Sign_up,logout_view,activate_user,admin_dashboard,assign_role,create_group,group_list



urlpatterns = [
    path('signup/', Sign_up, name='signup'),
    path('sign-in/', Sign_in, name='sign-in'),
    path('logout/', logout_view, name='logout'),
    path('activate/<int:user_id>/<str:token>/',activate_user),
    path('admin/dashboard/',admin_dashboard,name='admin-dashboard'),
    path('admin/<int:user_id>/assign-role',assign_role,name='assign-role'),
    path('admin/create-group/',create_group,name='create-group'),
    path('admin/group-list/', group_list , name='group-list')

]