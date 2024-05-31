from django.utils import timezone
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class Admin(models.Model):
    admin_id = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)

    def clean(self):
        super().clean()
        if not self.admin_id:
            raise ValidationError(_('Admin ID cannot be empty'))
        if not self.password:
            raise ValidationError(_('Password cannot be empty'))

    def __str__(self):
        return self.admin_id


class Employee(models.Model):
    name = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    employee_id = models.CharField(max_length=100, unique=True)
    address = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15)
    destination = models.CharField(max_length=100, blank=True, null=True)
    date_of_birth = models.DateField()
    date_of_joining = models.DateField()
    email = models.EmailField(unique=True)
    newemail = models.EmailField(unique=True,null=True)
    password = models.CharField(max_length=100)
    designation = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    picture = models.ImageField(
        upload_to='employee_pictures/', blank=True, null=True)

    def __str__(self):
        return self.name


class Department(models.Model):
    name = models.CharField(max_length=100,unique=True)
    code = models.CharField(max_length=20, unique=True)
    head = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

# models.py


class Contact(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    mobile = models.CharField(max_length=15)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


# models.py


class Task(models.Model):
    PRIORITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    ]

    CATEGORY_CHOICES = [
        ('Work', 'Work'),
        ('Personal', 'Personal'),
        ('Errands', 'Errands'),
    ]

    title = models.CharField(max_length=100)
    description = models.TextField()
    assigned_to = models.ForeignKey(Employee, on_delete=models.CASCADE)
    deadline_date = models.DateField()
    deadline_time = models.TimeField()
    email = models.EmailField()
    created_at = models.DateTimeField(default=timezone.now)
    priority = models.CharField(
        max_length=10, choices=PRIORITY_CHOICES, default='Medium')
    category = models.CharField(
        max_length=20, choices=CATEGORY_CHOICES, default='Work')

    def __str__(self):
        return self.title


class FinishedTask(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    assigned_to = models.ForeignKey(Employee, on_delete=models.CASCADE)
    deadline_date = models.DateField()
    deadline_time = models.TimeField()
    email = models.EmailField()
    finished = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class EmployeeSignUp(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.name
