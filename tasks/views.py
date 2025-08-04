from django.http import HttpResponse
from django.shortcuts import render, redirect
from tasks.forms import TaskModelForm, TaskDetailModelForm 
from tasks.models import  Task, Project
from django.db.models import Q, Count 
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test,login_required,permission_required
from user.views import is_admin
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.views.generic.base import ContextMixin
from django.views.generic import ListView,DetailView,UpdateView
# Class based views are not used in this file:
class Greetings(View):
    greetings = "Hello, World!"
    
    def get(self,request):
        return HttpResponse(self.greetings)
    
class HiGreetings(Greetings):   
    greetings = "Hi, Everyone!"

class HelloSujon(Greetings):
    greetings="Hello SUjon"


class New(View):
    he="oi kera bro"
    
    def get(self,request):
        return HttpResponse(self.he)
    

# Create your views here.
def is_manager(user):
    return user.groups.filter(name='Manager').exists()
def is_employee(user):
    return user.groups.filter(name='Employee').exists()

@user_passes_test(is_manager,login_url='no-permission')
def manager_dashboard(request):
    tasks = Task.objects.select_related('details').prefetch_related('assigned_to').all()
    
    type=request.GET.get("type",'all')
     
    # Optimization
    counts=Task.objects.aggregate(  
            total=Count('id'),
            completed=Count('id',filter=Q(status="COMPLETED")),
            in_progress=Count('id',filter=Q(status="IN_PROGRESS")),
            pending=Count('id',filter=Q(status="PENDING"))
                                                              
    )
    # Retrieving task data
    base_query =Task.objects.select_related('details').prefetch_related('assigned_to')
    
    if type=='completed':
        tasks=base_query.filter(status="COMPLETED")
    elif type=='in-progress':
        tasks=base_query.filter(status="IN_PROGRESS")
    elif type== 'pending':
        tasks=base_query.filter(status="PENDING")
    elif type=='all':
        tasks=base_query.all()
    
    context={
        "tasks":tasks,
        "counts":counts
    }

    return render(request, "dashboard/manager_dashboard.html", context)

@user_passes_test(is_employee,login_url='no-permission')
def employee_dashboard(request):
    return render(request, "dashboard/user_deasborad.html")


def test(request):
    names = ["Mahmud", "Ahamed", "John", "Mr. X"]
    count = 0
    for name in names:
        count += 1
    context = {
        "names": names,
        "age": 23,
        "count": count
    }
    return render(request, 'test.html', context)

@login_required
@permission_required("tasks.add_task",login_url='no-permission')
def create_task(request):
    # employees = Employee.objects.all()
    task_form = TaskModelForm()  # For GET
    task_detail_form = TaskDetailModelForm()

    if request.method == "POST":
        task_form = TaskModelForm(request.POST)
        task_detail_form = TaskDetailModelForm(request.POST,request.FILES)

        if task_form.is_valid() and task_detail_form.is_valid():

            """            For       Model      Form        Data """
            task = task_form.save()
            task_detail = task_detail_form.save(commit=False)
            task_detail.task = task
            task_detail.save()

            messages.success(request, "Task Created Successfully")
            return redirect('create-task')

    context = {"task_form": task_form, "task_detail_form": task_detail_form}
    return render(request, "task_form.html", context)


# variable in list of decorators
create_decorators=[login_required,permission_required("tasks.add_task",login_url='no-permission')]
#  Convert in ClassView  .............
# @method_decorator(create_decorators,name="dispatch") 
#  tah hola loginRequiredmixin ata    holo amier user login nh korla sob nea asa sa 
class create_task(ContextMixin,LoginRequiredMixin,PermissionRequiredMixin,View):
    # permission Required
    permission_required='tasks.add_task'
    login_url='sign-in'
    # For Creating Task .....
    template_name="task_form.html"
    """ 
    0.CREATE_Task
    1.LoginRequiredMixin
    2.PermissionMixin
    """
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['task_form']=kwargs.get(TaskModelForm())
        context['task_detail_form'] = kwargs.get(
        'task_detail_form', TaskDetailModelForm())
        return context
    
    def get(self,request,*args,**kwargs):
        #   task_form = TaskModelForm()  # For GET
        #   task_detail_form = TaskDetailModelForm()
        #   context = {"task_form": task_form, "task_detail_form": task_detail_form}
          context = self.get_context_data()
          return render(request, self.template_name, context)


    def post(self,request,*args,**kwargs):
        task_form = TaskModelForm(request.POST)
        task_detail_form = TaskDetailModelForm(request.POST,request.FILES)

        if task_form.is_valid() and task_detail_form.is_valid():

            """            For       Model      Form        Data """
            task = task_form.save()
            task_detail = task_detail_form.save(commit=False)
            task_detail.task = task
            task_detail.save()

            messages.success(request, "Task Created Successfully")
            
            context = self.get_context_data( task_form=task_form, task_detail_form=task_detail_form)
            return render(request, self.template_name, context)
        


@login_required
@permission_required("tasks.change_task",login_url='no-permission')
def update_task(request, id):
    task = Task.objects.get(id=id)
    task_form = TaskModelForm(instance=task)  # For GET

    if task.details:
        task_detail_form = TaskDetailModelForm(instance=task.details)

    if request.method == "POST":
        task_form = TaskModelForm(request.POST, instance=task)
        task_detail_form = TaskDetailModelForm(
            request.POST, instance=task.details)

        if task_form.is_valid() and task_detail_form.is_valid():

            """ For Model Form Data """
            task_form.save()
            task_detail = task_detail_form.save(commit=False)
            task_detail.task = task
            task_detail.save()

            messages.success(request, "Task Updated Successfully")
            return redirect('update-task', id)

    context = {"task_form": task_form, "task_detail_form": task_detail_form}
    return render(request, "task_form.html", context)


#-------------------------------- Before in update_Task-----------------------------------------------------------------------
class UpdateTask(UpdateView):
    model=Task
    from_class=TaskModelForm()
    template_name='task_form.html'
    context_object_name='task'
    
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        task=self.get_object()
        
        if hasattr(self.object,'details') and self.object.details:
            context['task_detail_form'] = TaskDetailModelForm(
                instance=self.object.details)
        else:
            context['task_detail_form'] = TaskDetailModelForm()

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        task_form = TaskModelForm(request.POST, instance=self.object)

        task_detail_form = TaskDetailModelForm(
            request.POST, request.FILES, instance=getattr(self.object, 'details', None))

        if task_form.is_valid() and task_detail_form.is_valid():

            """ For Model Form Data """
            task = task_form.save()
            task_detail = task_detail_form.save(commit=False)
            task_detail.task = task
            task_detail.save()

            messages.success(request, "Task Updated Successfully")
            return redirect('update-task', self.object.id)
        return redirect('update-task', self.object.id)
            

@login_required
@permission_required("tasks.delete_task",login_url='no-permission')
def delete_task(request, id):
    if request.method == 'POST':
        task = Task.objects.get(id=id)
        task.delete()
        messages.success(request, 'Task Deleted Successfully')
        return redirect('manager-dashboard')
    else:
        messages.error(request, 'Something went wrong')
        return redirect('manager-dashboard')

# after in function view.......................................
@login_required
@permission_required("tasks.view_task",login_url='no-permission')
def view_task(request):
    projects = Project.objects.annotate(
        num_task=Count('tasks')).order_by('num_task')
    return render(request, "show_task.html", {"projects": projects})


# class based view in view.html
view_project_decorators = [login_required, permission_required(
    "projects.view_project", login_url='no-permission')]
# After in Class view .....................................
@method_decorator(view_project_decorators,name='dispatch')
class viewProject(ListView):
    model=Project
    context_object_name='projects'
    template_name='show_task.html'
    
    def get_queryset(self):
        queryset = Project.objects.annotate(
            num_task=Count('tasks')).order_by('num_task') 
        return queryset

# ----------------------               After in Task  detail   ------------------------------------------------------------------
@login_required
@permission_required("tasks.view_task",login_url='no-permission')
def task_detail(request,task_id):
    task=Task.objects.get(id=task_id)
    status_choices=Task.STATUS_CHOICES
    
    if request.method=='POST':
        selected_status=request.POST.get('task_status')
        # print(selected_status)
        task.status = selected_status
        task.save()
        return redirect('task_details',task.id)
    return render(request,'task_details.html',{"task":task,'status_choices':status_choices})

# ----------------------               Before in Task  detail   ------------------------------------------------------------------
task_details_decorators = [login_required, permission_required(
    "Task.task_details", login_url='no-permission')]
@method_decorator(task_details_decorators,name='dispatch')
class TaskDetail(DetailView):
    model=Task
    template_name='task_details.html'
    context_object_name='task'
    pk_url_kwarg='task_id'
    
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs) # {"task":task}
        context['status_choices'] = Task.STATUS_CHOICES #{{"task":task,'status_choices':status_choices}}
        return context
    
    def post(self,request,*args,**kwargs):
        task=self.get_object()
        selected_status=request.POST.get('task_status')
        # print(selected_status)
        task.status = selected_status
        task.save()
        return redirect('task_details',task.id)
        
@login_required
def dashboard(request):
    if is_manager(request.user):
     return redirect('manager-dashboard')
    elif is_employee(request.user):
        return redirect('user_deasborad')
    elif is_admin(request.user):
        return redirect("admin-dashboard")
    
    return redirect('no-permission')