from django.urls import path
from user.views import Sign_in, Sign_up,logout_view,activate_user,admin_dashboard,assign_role,create_group,group_list,CustomLoginView,ProfileView,ChangePassword,CustomPasswordResetView,CustomPasswordConfirmResetView
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView ,PasswordChangeView,PasswordChangeDoneView


urlpatterns = [
    path('signup/', Sign_up, name='signup'),
    # path('sign-in/', LoginView.as_view(template_name='admin/user_list.html'), name='sign-in'), => ata holo jokon register page kono appllicatrion thakva ata use korta hova
    path('sign-in/',CustomLoginView.as_view(), name='sign-in'),
    # path('sign-in/', Sign_in, name='sign-in'),
    # path('logout/', logout_view, name='logout'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('activate/<int:user_id>/<str:token>/',activate_user),
    path('admin/dashboard/',admin_dashboard,name='admin-dashboard'),
    path('admin/<int:user_id>/assign-role',assign_role,name='assign-role'),
    path('admin/create-group/',create_group,name='create-group'),
    path('admin/group-list/', group_list , name='group-list'),
    path('profile/',ProfileView.as_view(),name='profile'),
    path('password-change/',ChangePassword.as_view(),name='password_change'),
    path('password-change/done/',PasswordChangeDoneView.as_view(template_name='accounts/password_change_done.html')),
    path('password-reset/',CustomPasswordResetView.as_view(),name='password-reset'),
    path('password-reset-confirm/<uidb64>/<token>',CustomPasswordConfirmResetView.as_view(),name='password_reset_confirm')

]