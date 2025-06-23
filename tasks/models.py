from django.db import models


# Create your models here.

class Employee(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField()
class Task(models.Model):
    assigned_to=models.ManyToManyField(Employee,related_name="task")
    project = models.ForeignKey("Project", on_delete=models.CASCADE, default=1 , related_name="tasks")
    # one to many relation ship 
    title = models.CharField(max_length=250)
    description = models.TextField()
    due_date = models.DateField()
    is_completed = models.BooleanField(default=False)
    create_at = models.DateField(auto_now_add=True)
    update_at = models.DateField(auto_now=True)


# one to one
# one to many
# many to many


class TaskDetail(models.Model):
    HIGH = "H"
    MEDIUM = "M"
    LOW = "L"
    PRIORITY_OPTIONS = ((HIGH, "HIGH"), (MEDIUM, "MEDIUM"), (LOW, "LOW"))
    # one to Relational
    task = models.OneToOneField(
        Task, on_delete=models.CASCADE,
        related_name='details'
        
    )  # jodi Task nh taka tah hola kao taka nh
    assigned_to = models.CharField(max_length=100)
    priority = models.CharField(max_length=1, choices=PRIORITY_OPTIONS, default=LOW)


class Project(models.Model):
    name = models.CharField(max_length=100)
    start_date = models.DateField()
