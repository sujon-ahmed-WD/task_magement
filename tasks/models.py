from django.db import models
import datetime
from django.db.models.signals import post_save , pre_save, m2m_changed,post_delete
from django.dispatch import receiver
from django.core.mail import send_mail

class Employee(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField()
    def __str__(self):
        return self.name
# from tasks.models import *
class Task(models.Model):
    
    STATUS_CHOICES =[
        ('PENDING','Pending'),
        ('IN Progress','in Progress'),
        ('COMPLETED','Complied')
    ]
    assigned_to=models.ManyToManyField(Employee, related_name="tasks")
    project = models.ForeignKey("Project", on_delete=models.CASCADE, default=1 , related_name="tasks")
    title = models.CharField(max_length=250)
    description = models.TextField()
    due_date = models.DateField()
    status=models.CharField(
        max_length=15,choices=STATUS_CHOICES,default="PENDING"
    )
    is_completed = models.BooleanField(default=False)
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
    
    # assigned_to = models.CharField(max_length=100)
    priority = models.CharField(max_length=1, choices=PRIORITY_OPTIONS, default=LOW)
    notes=models.TextField(blank=True,null=True)

    def __str__(self):
        return f"Details from Tasks {self.task.title}"
    

# Signals
#  EMail patasi 
@receiver(m2m_changed, sender=Task.assigned_to.through)
def notify_employees_on_task_creation(sender, instance, action,**kwargs):
    if action== 'post_add':
        assigned_emails = [emp.email for emp in instance.assigned_to.all()]
        send_mail(
            "Subject here",
            f"You have been assigned to task :{instance.title}",
            "sujonahmed.22.03@gmail.com",
            assigned_emails
        )
        # Post delete
@receiver(post_delete,sender=Task)
def  delete_associate_details(sender,instance,**kwargs):
    if instance.details:
        print(instance)
        instance.details.delete()
        print("DELETE SUCCESSFULLY")