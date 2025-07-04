# Generated by Django 5.2.3 on 2025-06-23 12:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0006_alter_task_assigned_to'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='assigned_to',
            field=models.ManyToManyField(related_name='task', to='tasks.employee'),
        ),
        migrations.AlterField(
            model_name='task',
            name='project',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='tasks.project'),
        ),
    ]
