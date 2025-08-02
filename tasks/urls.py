from django.urls import path
from tasks.views import manager_dashboard, employee_dashboard, test, create_task, view_task, update_task, delete_task,task_detail,Greetings,HiGreetings,HelloSujon,New,viewProject,TaskDetail,dashboard
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('manager_dashboard/', manager_dashboard,name="manager-dashboard"),
    path('user-dashboard/', employee_dashboard),
    path('test/', test),
    # path('create-task/', create_task,name='create-task'),
    path('create-task/',create_task.as_view(),name='create-task'),
    # path('view_task/', viewme='view-task'),
    path('view_task/', viewProject.as_view(),name='view-task'),
    # path('task/<int:task_id>/details',task_detail,name='task-details'),
    path('task/<int:task_id>/details',TaskDetail.as_view(),name='task-details'),
    path('update-task/<int:id>',update_task,name='update-task'),
    path('delete-task/<int:id>/', delete_task, name='delete-task'),
    path('dashboard/',dashboard,name='dashboard'),
    path('greetings/',HelloSujon.as_view(greetings="Aslamolikum Sujon"), name='greetings'),
    
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
