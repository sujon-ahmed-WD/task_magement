from tasks.models import Task
from django.db.models.signals import post_save , pre_save, m2m_changed,post_delete
from django.dispatch import receiver
from django.core.mail import send_mail
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