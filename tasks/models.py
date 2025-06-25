from django.db import models
class Employee(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField()

    def __str__(self):
        return self.name

class Task(models.Model):
    assigned_to=models.ManyToManyField(Employee, related_name="tasks")
    project = models.ForeignKey("Project", on_delete=models.CASCADE, default=1 , related_name="tasks")
    title = models.CharField(max_length=250)
    description = models.TextField()
    due_date = models.DateField()
    is_completed = models.BooleanField(default=False)
    create_at = models.DateField(auto_now_add=True)
    update_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.title

class Project(models.Model):
    name = models.CharField(max_length=100)

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
    assigned_to = models.CharField(max_length=100)
    priority = models.CharField(max_length=1, choices=PRIORITY_OPTIONS, default=LOW)

    def __str__(self):
        return f"{self.task.title} - {self.get_priority_display()}"