from .models import Task, FinishedTask
from .models import EmployeeSignUp
from django.contrib import admin
from .models import Department, Employee, Admin, Contact, Task, FinishedTask
from .forms import DepartmentForm


class AdminAdmin(admin.ModelAdmin):
    list_display = ['admin_id']


admin.site.register(Admin)

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'department', 'employee_id', 'address', 'contact_number',
                    'destination', 'date_of_birth', 'date_of_joining', 'email','newemail', 'designation', 'description')

# admin.py


@admin.register(EmployeeSignUp)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')
    # Customize admin interface as needed


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    form = DepartmentForm


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    # Customize the displayed fields if needed
    list_display = ['first_name', 'last_name',
                    'email', 'mobile', 'message', 'created_at']


# admin.py


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'assigned_to',
                    'deadline_date', 'deadline_time', 'email', 'priority', 'category']


@admin.register(FinishedTask)
class FinishedTaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'assigned_to',
                    'deadline_date', 'deadline_time', 'email', 'finished']
