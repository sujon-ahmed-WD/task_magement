from django.db import models
import datetime
from django.contrib.auth.models import User



# from tasks.models import *
class Task(models.Model):
    
    STATUS_CHOICES =[
        ('PENDING','Pending'),
        ('IN Progress','in Progress'),
        ('COMPLETED','Complied')
    ]
    # assigned_to=models.ManyToManyField(Employee, related_name="tasks")
    assigned_to=models.ManyToManyField(User,related_name='tasks')
    project = models.ForeignKey("Project", on_delete=models.CASCADE, default=1 , related_name="tasks")
    title = models.CharField(max_length=250)
    description = models.TextField()
    due_date = models.DateField()
    status=models.CharField(
        max_length=15,choices=STATUS_CHOICES,default="PENDING"
    )
    create_at = models.DateField(auto_now_add=True)
    update_at = models.DateField(auto_now=True)
    
    def __str__(self):
        return self.title


def get_default_start_date():
    return datetime.date(2025, 6, 5)

class Project(models.Model):
    name = models.CharField(max_length=100)
    # description = models.TextField(default="No description")
    start_date = models.DateField(default=get_default_start_date)

    def __str__(self):
        return self.name

class TaskDetail(models.Model):
    HIGH = "H"
    MEDIUM = "M"
    LOW = "L"
    PRIORITY_OPTIONS = ((HIGH, "HIGH"), (MEDIUM, "MEDIUM"), (LOW, "LOW"))

    task = models.OneToOneField(
        Task, on_delete=models.CASCADE,
        related_name='details'
    )
    
    asset=models.ImageField(upload_to='tasks-asset',blank=True,null=True)
    priority = models.CharField(max_length=1, choices=PRIORITY_OPTIONS, default=LOW)
    notes=models.TextField(blank=True,null=True)

    def __str__(self):
        return f"Details from Tasks {self.task.title}"
    

# Signals
#  EMail palais 
