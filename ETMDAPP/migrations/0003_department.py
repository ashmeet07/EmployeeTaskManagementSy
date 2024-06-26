# Generated by Django 4.2.5 on 2024-04-05 18:25

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("ETMDAPP", "0002_employee"),
    ]

    operations = [
        migrations.CreateModel(
            name="Department",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("code", models.CharField(max_length=20)),
                ("head", models.CharField(max_length=100)),
                ("location", models.CharField(max_length=100)),
                ("description", models.TextField()),
            ],
        ),
    ]
