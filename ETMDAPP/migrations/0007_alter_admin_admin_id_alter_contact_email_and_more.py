# Generated by Django 4.2.5 on 2024-04-18 14:10

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("ETMDAPP", "0006_task_email"),
    ]

    operations = [
        migrations.AlterField(
            model_name="admin",
            name="admin_id",
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name="contact",
            name="email",
            field=models.EmailField(max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name="department",
            name="code",
            field=models.CharField(max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name="employee",
            name="email",
            field=models.EmailField(max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name="employee",
            name="employee_id",
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
