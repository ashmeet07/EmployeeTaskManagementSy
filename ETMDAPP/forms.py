# forms.py
from .models import Task, Employee
from .models import Task
from .models import Contact
from .models import Department
from django import forms
from .models import Employee

from django import forms
from .models import Task, Contact, Department, Employee

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = '__all__'


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['first_name', 'last_name', 'email', 'mobile', 'message']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Enter first name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Enter last name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Enter email'}),
            'mobile': forms.TextInput(attrs={'placeholder': 'Enter mobile number'}),
            'message': forms.Textarea(attrs={'placeholder': 'Enter your message'}),
        }


# forms.py


class TaskForm(forms.ModelForm):
    email = forms.EmailField(required=False, widget=forms.TextInput(
        attrs={'placeholder': 'Search by Email'}))
    title = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Enter task title'}))
    description = forms.CharField(widget=forms.Textarea(
        attrs={'placeholder': 'Enter task description'}))
    assigned_to = forms.ModelChoiceField(
        queryset=Employee.objects.all(), empty_label="Select Employee")
    deadline_date = forms.DateField(widget=forms.DateInput(
        attrs={'placeholder': 'Select deadline date', 'class': 'datepicker'}))
    deadline_time = forms.TimeField(widget=forms.TimeInput(
        attrs={'placeholder': 'Select deadline time', 'class': 'form-control timepicker'}))
    priority = forms.ChoiceField(choices=Task.PRIORITY_CHOICES)
    category = forms.ChoiceField(choices=Task.CATEGORY_CHOICES)

    class Meta:
        model = Task
        fields = ['title', 'description', 'assigned_to', 'deadline_date',
                  'deadline_time', 'email', 'priority', 'category']


# forms.py


class EmployeeSignUpForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    # Add additional form fields here as needed
