from django.urls import path
from tasks.views import manager_dashboard,user_dashboard,test,create_task

urlpatterns = [
<<<<<<< HEAD
    path("manager_dashboard/",manager_dashboard),
    path("user_dashboard/",user_dashboard),
    path("test/",test),
    path("create_task/",create_task)
     
=======
    path("show_task/",show_task),
    path("show_task/<int:id>",show_specific_task)
    
>>>>>>> 9c622f7e7207656ec39c25138b911d052cb417e1
]