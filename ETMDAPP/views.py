from django.core.exceptions import ValidationError
import json
from django.http import JsonResponse
from .models import EmployeeSignUp
from .utils import (
    generate_task_distribution_plot,
    generate_remaining_tasks_plot,
    generate_task_deadlines_table,
    generate_completed_tasks_over_time_plot,
    generate_employee_performance_plot,
    generate_task_description_wordcloud,
    generate_completion_rate_by_employee_plot,
    generate_task_distribution_by_category_plot,
    generate_task_distribution_by_priority_plot,
    # generate_task_duration_distribution_plot
)
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import FinishedTask
from django.shortcuts import redirect, render, get_object_or_404
from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import redirect, render
from .utils import send_email_to_employee
from .models import Task
from .models import EmployeeSignUp  # Import the Employee model
from .models import Task, FinishedTask
from .forms import TaskForm
from .models import Employee, Task
import csv
from .forms import ContactForm
from .models import Contact
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .forms import DepartmentForm
from .models import Department
from .forms import EmployeeForm
from .forms import EmployeeForm  # Import the form
from django.core.files.storage import FileSystemStorage
from .models import Employee
from django.shortcuts import render, redirect
from .models import Admin
from django.shortcuts import render

# Create your views here.

def HOME(request):
    return render(request,"HOME.html")


def REGIEMP(request):
    departments = Department.objects.all()

    if request.method == "POST":
        try:
            # Retrieve form data
            name = request.POST.get("firstname")
            department = request.POST.get("department")
            employee_id = request.POST.get("id")
            address = request.POST.get("address")
            contact_number = request.POST.get("number")
            destination = request.POST.get("dest")
            date_of_birth = request.POST.get("dob")
            date_of_joining = request.POST.get("doj")
            email = request.POST.get("email")
            newemail = request.POST.get("newemail")
            password = request.POST.get("pass")
            designation = request.POST.get("des")
            description = request.POST.get("desc")

            # Save uploaded picture
            if 'pictureInput' in request.FILES:
                picture = request.FILES['pictureInput']
                fs = FileSystemStorage()
                filename = fs.save(picture.name, picture)
                picture_url = fs.url(filename)
            else:
                picture_url = None

            # Send email to employee
            send_email_to_employee(email, newemail)

            # Create and save Employee object
            employee = Employee.objects.create(
                name=name,
                department=department,
                employee_id=employee_id,
                address=address,
                contact_number=contact_number,
                destination=destination,
                date_of_birth=date_of_birth,
                date_of_joining=date_of_joining,
                email=email,
                newemail=newemail,
                password=password,
                designation=designation,
                description=description,
                picture=picture_url  # Assign the URL of the uploaded picture
            )

            # Redirect to the admin dashboard after successful registration
            return redirect("AdminDashboard")
        except Exception as e:
            # Handle any exception and return an error response
            error_message = "An error occurred while processing your request."
            return render(request, "error.html", {'error_message': error_message})

    # Render the registration form template for GET requests
    return render(request, "REGIEMP.html", {'departments': departments})


def employeesignuplogin(request):
    if request.method == "POST":
        email = request.POST.get("LOGINEmail")
        password = request.POST.get("LOGINPassword")

        # Check if email and password are provided for login
        if email and password:
            try:
                user = EmployeeSignUp.objects.get(email=email)
                if password == user.password:
                    # Authentication successful
                    print("Authentication successful")
                    # Replace 'EMPDashboard' with the actual URL name for the employee dashboard
                    request.session['EmployeeEmail'] = email
                    request.session['EmployeeUsername'] = user.name
                    return redirect("EMPDashboard")
                else:
                    # Authentication failed - invalid password
                    print("Authentication failed: Invalid password")
                    # Render login page with error message
                    return render(request, "LOGIN.html", {'error_message': "Invalid email or password"})
            except EmployeeSignUp.DoesNotExist:
                # Authentication failed - user not found
                print("Authentication failed: User not found")
                # Render login page with error message
                return render(request, "LOGIN.html", {'error_message': "Invalid email or password"})
        else:
            # Signup process
            name = request.POST.get("Name")
            email = request.POST.get("Email")
            password = request.POST.get("Password")

            # Check if email and password are provided for signup
            if email and password:
                # Check if the email is already registered
                if EmployeeSignUp.objects.filter(email=email).exists():
                    # Render signup page with error message
                    return render(request, "LOGIN.html", {'error_message': "Email is already registered. Please use a different email."})

                # Create a new user instance
                new_user = EmployeeSignUp(
                    name=name, email=email, password=password)
                # Save the new user to the database
                new_user.save()

                # Redirect to login page after successful signup
                # Render login page with success message
                return render(request, "LOGIN.html", {'success_message': "Sign up successful! Please log in"})

            else:
                # No email or password provided for signup or login
                print("No email or password provided")
                # Render login page with error message
                return render(request, "LOGIN.html", {'error_message': "Please provide email and password"})

    # Render the login page for GET requests
    return render(request, "LOGIN.html")


def handle_login(request, data):
    email = data["Email"]
    password = data["Password"]

    # Authenticate the user
    user = authenticate(request, email=email, password=password)

    if user is not None:
        # Login the user
        login(request, user)
        # Redirect to a success page or homepage
        return redirect("home")
    else:
        # If authentication fails, display an error message for login
        error_message = "Invalid email or password. Please try again."
        return render(request, "login.html", {"error_message": error_message})


def employee_list(request):
    try:
        query = request.GET.get('q')
        if query:
            employees = Employee.objects.filter(email__icontains=query)
        else:
            employees = Employee.objects.all()
        return render(request, 'emplist.html', {'employees': employees, 'query': query})
    except ValidationError as ve:
        # Handle validation errors
        error_message = "Validation Error: {}".format(ve)
        return render(request, "error.html", {'error_message': error_message})
    except Exception as e:
        # Handle other exceptions
        error_message = "An error occurred while processing your request."
        return render(request, "error.html", {'error_message': error_message})



def search_employee(request):
    query_email = request.GET.get('email')
    query_emp_id = request.GET.get('emp_id')

    employees = Employee.objects.all()  # Default queryset

    if query_email:
        employees = employees.filter(email__icontains=query_email)
    if query_emp_id:
        employees = employees.filter(employee_id__icontains=query_emp_id)

    return render(request, 'emplist.html', {'employees': employees, 'query_email': query_email, 'query_emp_id': query_emp_id})


def delete_employee(request, pk):
    employee = Employee.objects.get(pk=pk)
    employee.delete()
    return redirect('AdminDashboard')


def edit_employee(request, pk):
    employee = Employee.objects.get(pk=pk)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('AdminDashboard')
    else:
        form = EmployeeForm(instance=employee)
    return render(request, 'editemp.html', {'form': form})

def ABOUT(request):
    return render(request, "ABOUT.html")


def EMPDASHBOARD(request):
    try:
        # Get email from session
        email = request.session.get("EmployeeEmail")

        if email:
            # Filter tasks by assigned_to email
            tasks = Task.objects.filter(email=email)

            # Get total number of tasks
            total_tasks = tasks.count()

            # Get number of in-progress tasks with high priority
            in_progress_tasks = tasks.filter(
                priority='High',
            ).count()

            # Get number of completed tasks
            completed_tasks = FinishedTask.objects.filter(
                email=email, finished=True
            ).count()

            # Render the template with counts
            return render(request, "EMPDashboard.html", {
                'total_tasks': total_tasks,
                'in_progress_tasks': in_progress_tasks,
                'completed_tasks': completed_tasks,
            })
        else:
            # Handle the case where email is not found in the session
            error_message = "Session data missing. Please log in again."
            return render(request, "error.html", {'error_message': error_message})
    except Exception as e:
        # Handle other exceptions
        error_message = "An error occurred while processing your request."
        return render(request, "error.html", {'error_message': error_message})
    
def REGIDMENT(request):
    return render(request, "REGIDMENT.html")

from django.shortcuts import redirect


def logout(request):
    try:
        # Check if the 'admin_email' session variable exists
        if 'admin_email' in request.session:
            # Delete the 'admin_email' session variable
            del request.session['admin_email']

        # Check if other session variables exist and delete them based on conditions
        if 'EmployeeEmail' in request.session:
            del request.session['EmployeeEmail']
        if 'EmployeeUsername' in request.session:
            del request.session['EmployeeUsername']

        # Redirect to the home page after logout
        # Replace 'HOME' with the name of your home page URL pattern
        return redirect('HOME')
    except Exception as e:
        # Handle any exceptions
        error_message = "An error occurred while logging out."
        return render(request, "error.html", {'error_message': error_message})

 
def ADMINLOGIN(request):
    if request.method == "POST":
        admin_id = request.POST.get("email")
        password = request.POST.get("password")

        try:
            # Retrieve admin data based on admin_id
            admin = Admin.objects.get(admin_id=admin_id)
        except Admin.DoesNotExist:
            return redirect("ADMINLOGIN")

        # Check if the provided password matches the admin's password
        if admin.password == password:
            # Create session for admin's email
            request.session['admin_email'] = admin.admin_id

            # Redirect to admin dashboard or render a template
            total_employees = Employee.objects.count()
            return redirect("AdminDashboard")
        else:
            return render(request, "adminlogin.html", {"error_message": "Invalid credentials"})

    # Get the admin email from the session, if available
    admin_email = request.session.get('admin_email', None)

    return render(request, "adminlogin.html", {"admin_email": admin_email})


def AdminDashboard(request):
    try:
        # Check if the 'admin_email' session variable exists
        admin_email = request.session.get('admin_email', None)
        if admin_email is None:
            return redirect('ADMINLOGIN')

        # Total count of employees and departments
        total_employees = Employee.objects.count()
        total_departments = Department.objects.count()

        # Count of finished tasks
        finished_tasks_count = FinishedTask.objects.count()

        # Count of assigned tasks (assuming each employee can have multiple tasks)
        assigned_tasks_count = Task.objects.count()

        return render(request, "AdminDashboard.html", {
            'total_employees': total_employees,
            'total_departments': total_departments,
            'finished_tasks_count': finished_tasks_count,
            'assigned_tasks_count': assigned_tasks_count,
            'admin_email': admin_email,
        })
    except Exception as e:
        # Handle any exceptions
        error_message = "An error occurred while loading the admin dashboard."
        return render(request, "error.html", {'error_message': error_message})


def REGIDMENT(request):
    try:
        # Check if the 'admin_email' session variable exists
        admin_email = request.session.get('admin_email', None)
        if admin_email is None:
            return redirect('ADMINLOGIN')

        if request.method == 'POST':
            form = DepartmentForm(request.POST)
            if form.is_valid():
                form.save()
                # Redirect to a page showing department list
                return redirect('AdminDashboard')
        else:
            form = DepartmentForm()
        return render(request, 'REGIDMENT.html', {'form': form, 'admin_email': admin_email})
    except Exception as e:
        # Handle any exceptions
        error_message = "An error occurred while processing department registration."
        return render(request, "error.html", {'error_message': error_message})


def department_list(request):
    departments = Department.objects.all()
    total_departments = departments.count()
    context = {
        'departments': departments,
        'total_departments': total_departments
    }
    return render(request, 'Dlist.html', context)


# views.py


def edit_department(request, department_id):
    department = get_object_or_404(Department, pk=department_id)
    if request.method == 'POST':
        form = DepartmentForm(request.POST, instance=department)
        if form.is_valid():
            form.save()
            # Redirect to department list page after successful edit
            return redirect('department_list')
    else:
        form = DepartmentForm(instance=department)
    return render(request, 'edit_department.html', {'form': form})


def delete_department(request, department_id):
    department = get_object_or_404(Department, pk=department_id)
    if request.method == 'POST':
        department.delete()
        # Redirect to department list page after successful delete
        return redirect('department_list')
    return render(request, 'AdminDashboard', {'department': department})



def search_department(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        departments = Department.objects.filter(name__icontains=name)
        return render(request,'Dlist.html', {'departments': departments})
# views.pyrender

# views.py


# views.py
def CONTACT(request):
    try:
        if request.method == 'POST':
            form = ContactForm(request.POST)
            if form.is_valid():
                # Save form data
                form.save()
                # Redirect to the home page after successful form submission
                return redirect('HOME')
        else:
            form = ContactForm()
        return render(request, 'CONTACT.html', {'form': form})
    except Exception as e:
        # Handle any exceptions
        error_message = "An error occurred while processing the contact form."
        return render(request, "error.html", {'error_message': error_message})

def assign_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        print(form)
        if form.is_valid():
            form.save()  # Save the form data to the database
            return redirect('AdminDashboard')  # Redirect to a success page
    else:
        form = TaskForm()
    return render(request, 'assigntask.html', {'form': form})


def task_des(request):
    # Get employees who have been assigned tasks
    employees_with_tasks = Employee.objects.filter(
        task__isnull=False).distinct()
    return render(request, 'TaskDes.html', {'employees': employees_with_tasks})

def assigned_tasks(request):
    # Get employees who have been assigned tasks
    employees_with_tasks = Employee.objects.filter(
        task__isnull=False).distinct()
    return render(request, 'taskemployeelist.html', {'employees': employees_with_tasks})


def finished_tasks(request):
    finished_tasks = FinishedTask.objects.all()
    return render(request, 'finished_tasks.html', {'finished_tasks': finished_tasks})


def TaskReport(request):
    # Generate plots
    generate_task_distribution_plot()
    generate_remaining_tasks_plot()
    generate_task_deadlines_table()
    generate_completed_tasks_over_time_plot()
    generate_employee_performance_plot()
    generate_task_description_wordcloud()
    generate_completion_rate_by_employee_plot()
    generate_task_distribution_by_category_plot()
    generate_task_distribution_by_priority_plot()
    # generate_task_duration_distribution_plot()    

    # Add any additional context data you want to pass to the template
    context = {}

    # Render the template
    return render(request, 'TaskReport.html', context)



def mark_task_finished(request, task_id, email):
    if request.method == 'POST':
        # Retrieve the task associated with the provided ID
        task = get_object_or_404(Task, pk=task_id, assigned_to__email=email)

        # Create a FinishedTask object with the details of the original task
        finished_task = FinishedTask.objects.create(
            title=task.title,
            description=task.description,
            assigned_to=task.assigned_to,
            deadline_date=task.deadline_date,
            deadline_time=task.deadline_time,
            email=task.email,
            finished=True  # Mark the task as finished
        )

        # Delete the original task
        task.delete()

        # Redirect the user to a success page or another appropriate URL
        return redirect('AdminDashboard')
    else:
        # Handle GET requests appropriately, if needed
        pass


def DEV(request):
    return render(request, "Developers.html")


def task_end_dates(request):
    tasks = Task.objects.all()
    return render(request, 'taskenddate.html', {'tasks': tasks})

def EMPAccount(request):
    return render(request,"EMPAccount.html")


def TaskDashboard(request):
    # Assuming you get email from session
    email = request.session.get("EmployeeEmail")

    # Filter tasks assigned to the employee (using assigned_to relationship)
    assigned_tasks = Task.objects.filter(email=email)

    total_tasks = assigned_tasks.count()
    completed_tasks = FinishedTask.objects.filter(
        email=email, finished=True).count()

    # Calculate completion rate with potential zero division handling and 50% for equal values
    completion_rate = 0
    if total_tasks > 0:
        if total_tasks == completed_tasks:
            completion_rate = 50  # Set 50% for equal completed and total tasks
        else:
            completion_rate = round((completed_tasks / total_tasks) * 100,2)
    performance_rate = completion_rate
    NoOfTasks=total_tasks + completed_tasks

    context = {
        'completion_rate': completion_rate,
        'total_tasks': NoOfTasks,
        'performance_rate': performance_rate,
    }

    return render(request, "EMPTaskDashboard.html", context)


def EMPTaskEndDate(request):
    try:
        # Check if the 'EmployeeEmail' session variable exists
        email = request.session.get("EmployeeEmail", None)
        if email:
            tasks = Task.objects.filter(email=email)
        else:
            tasks = []

        return render(request, 'EMPTaskEndDate.html', {'tasks': tasks})
    except Exception as e:
        # Handle any exceptions
        error_message = "An error occurred while loading the employee tasks."
        return render(request, "error.html", {'error_message': error_message})



def EmployeeTask(request):
    try:
        # Check if the 'EmployeeEmail' session variable exists
        email = request.session.get("EmployeeEmail", None)
        username = request.session.get("EmployeeUsername", None)

        if email:
            tasks = Task.objects.filter(email=email)
        else:
            tasks = []

        return render(request, 'EmployeeTask.html', {'email': email, 'tasks': tasks, 'username': username})
    except Exception as e:
        # Handle any exceptions
        error_message = "An error occurred while loading the employee tasks."
        return render(request, "error.html", {'error_message': error_message})
