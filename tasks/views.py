from django.http import HttpResponse
from django.shortcuts import render
from tasks.froms import TaskForm
from tasks.models import Employee,Task
 

# Create your views here.
def manager_dashboard(request):
    return render(request,'deshborad/manager_desborard.html')

def user_dashboard(request):
    return render(request,'deshborad/user_deasborad.html')

def create_task(request):
    # ---------------jokn load hoba .--------------------
    employees = Employee.objects.all()  
    form=TaskForm(employees=employees)  
    #----------------------- jokon amier employee data deva oi kaj golo hoba akna  // ba data goloo submet button CLick korobo//
    if request.method =="POST": 
        form=TaskForm(request.POST,employees=employees) # from sov employee data debo 
        if form.is_valid(): # if jodi data valid hoy then tomi from asva 
            data=form.cleaned_data
            title=data.get('title')
            decripation=data.get('descripation')
            due_date=data.get('due_date')
            assigned_to=data.get('assigned_to')
            
            task= Task.objects.create(title=title,decripation=decripation,due_date=due_date)
            
            # Assing employe to tasks
            for emp_id in assigned_to:
                employee=Employee.objects.get(id=emp_id)
                task.assigned_to.add(employee)
            
            return HttpResponse("Task Added successfully ")
    
    
    
    context={"form":form}
    return render(request,'deshborad/task_from.html',context)
     

def test(request):
    # names=["Maud","Ahmed","John","tus tus"]
    # count=0
    # for name in names:
    #     count+=1
    # context={
    #     "names":["Maud","Ahmed","John","tus tus"],
    #     "age":22
         
    # }
    context={
        "names":["M","tu","ahm","tabu"],
        "age":22
    }
    return render(request,'test.html',context)
    


  