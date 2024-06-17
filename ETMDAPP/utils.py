# utils.py
from .models import Task, FinishedTask, Employee
import seaborn as sns
import matplotlib.colors as mcolors
import numpy as np
from django.db.models import Count
from django.core.mail import send_mail
from django.conf import settings
from .models import Task, FinishedTask
import matplotlib.pyplot as plt
from django_pandas.io import read_frame
from wordcloud import WordCloud
import pandas as pd
from .models import Task, FinishedTask
from django.db.models import Count
import datetime
from django.utils import timezone
import matplotlib
matplotlib.use('Agg')  # Use the 'Agg' backend which is non-interactive


# Import plotting functions from utils.py


# Rest of your views.py code...


def send_email_to_employee(email, new_email):
    """
    Sends a customized welcome email to the client upon signup.
    """
    # Extract email settings from Django settings
    from_email = settings.EMAIL_HOST_USER

    # Construct email subject and message
    subject = "Welcome to ETMD Pvt Ltd."
    message = f"""
    Dear {email},

    I trust this message finds you in good health. It is my distinct pleasure to welcome you to ETMD Pvt Ltd, an esteemed platform dedicated to excellence.

    Your participation is highly valued, and we are delighted to have you as part of our team.

    Your new email address for communication is: {new_email}

    ETMD Pvt Ltd, under the leadership of ETMD, Director, is committed to fostering a transformative and enriching experience. We firmly believe that your presence will contribute significantly to the vibrancy of our community.

    For any inquiries or assistance, please do not hesitate to reach out to ETMD directly at {from_email}.

    We appreciate your consideration of our invitation and eagerly anticipate the prospect of welcoming you into the ETMD Pvt Ltd community.

    Best regards,

    ETMD
    Director, ETMD Pvt Ltd
    {from_email}
    """
    send_mail(subject, message, from_email, [email], fail_silently=False)


def generate_task_distribution_plot():
    tasks = Task.objects.all()
    df_tasks = read_frame(tasks)

    # Ensure the 'assigned_to' field is the employee's name
    task_counts = df_tasks['assigned_to'].value_counts()

    # Sort task counts in descending order
    task_counts = task_counts.sort_values(ascending=False)

    plt.figure(figsize=(12, 8))

    # Create gradient colormap from dark blue to light blue
    colormap = plt.cm.Blues
    norm = mcolors.Normalize(vmin=0, vmax=len(task_counts))
    colors = [colormap(norm(i)) for i in range(len(task_counts))]

    bars = task_counts.plot(kind='bar', color=colors, edgecolor='black')

    plt.title('Task Distribution Among Employees', fontsize=16)
    plt.xlabel('Employee', fontsize=14)
    plt.ylabel('Number of Tasks', fontsize=14)

    # Set y-axis to integer scale
    plt.gca().yaxis.set_major_locator(plt.MaxNLocator(integer=True))

    plt.xticks(rotation=45, ha='right', fontsize=12)
    plt.yticks(fontsize=12)

    # Calculate percentiles
    percentiles = np.percentile(task_counts, [25, 50, 75])

    # Categorize tasks based on percentiles
    categories = []
    for count in task_counts:
        if count >= percentiles[2]:
            categories.append('Heavy workload')
        elif count >= percentiles[1]:
            categories.append('Moderate workload')
        else:
            categories.append('Light workload')

    # Create legend with colors corresponding to the bars
    legend_handles = []
    for i, (label, color) in enumerate(zip(categories, colors)):
        if label not in legend_handles:
            legend_handles.append(label)
            plt.bar(0, 0, color=color, label=label)  # Dummy bars for legend

    plt.legend(loc='upper right', fontsize=12)

    plt.tight_layout()
    plt.savefig('ETMDAPP/static/CHARTS/task_distribution.png')
    plt.close()


def generate_remaining_tasks_plot():
    tasks = Task.objects.all()
    total_tasks = tasks.count()
    finished_tasks = FinishedTask.objects.filter(finished=True).count()
    remaining_tasks = total_tasks - finished_tasks

    # Calculate percentages
    finished_percentage = (finished_tasks / total_tasks) * 100
    remaining_percentage = 100 - finished_percentage

    labels = [f'Finished ({finished_percentage:.1f}%)',
              f'Remaining ({remaining_percentage:.1f}%)']
    sizes = [finished_tasks, remaining_tasks]
    colors = ['lightblue', 'lightcoral']

    # Explode the first slice to highlight it
    explode = (0.1, 0)

    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(aspect="equal"))

    # Create pie chart
    wedges, texts, autotexts = ax.pie(sizes, explode=explode, labels=labels, colors=colors,
                                      autopct='%1.1f%%', startangle=140, shadow=True)

    # Customizing text properties
    ax.legend(wedges, labels, loc="upper left", fontsize=10,
              facecolor='white', edgecolor='black', shadow=True)
    plt.setp(autotexts, size=12, weight="bold")

    plt.title('Remaining Tasks', fontsize=16)

    # Save the plot
    plt.savefig('ETMDAPP/static/CHARTS/remaining_tasks.png')
    plt.close()


def generate_task_deadlines_table():
    # Get the current date and time
    current_date = timezone.now().date()

    # Calculate the date for the next Monday
    next_monday = current_date + datetime.timedelta(days=(7 - current_date.weekday()))

    # Calculate the date for the following Monday
    following_monday = next_monday + datetime.timedelta(weeks=1)

    # Filter tasks whose deadline is within the coming next week starting from Monday
    tasks = Task.objects.filter(deadline_date__gte=next_monday, deadline_date__lt=following_monday)
    
    # Prepare data for the table
    deadlines_data = [{'deadline_date': task.deadline_date, 'num_tasks': Task.objects.filter(deadline_date=task.deadline_date).count()} for task in tasks]

    return deadlines_data


def generate_completed_tasks_over_time_plot():
    finished_tasks = FinishedTask.objects.filter(finished=True)
    df_finished_tasks = read_frame(finished_tasks)

    plt.figure(figsize=(10, 6))
    task_counts = df_finished_tasks['deadline_date'].value_counts(
    ).sort_index()
    task_counts.plot(marker='o', color='skyblue')

    plt.title('Completed Tasks Over Time')
    plt.xlabel('Deadline Date')
    plt.ylabel('Number of Tasks')
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Add legend
    plt.legend(['Completed Tasks'], loc='upper right', facecolor='lightgrey')

    plt.savefig('ETMDAPP/static/CHARTS/completed_tasks_over_time.png')
    plt.close()


def generate_employee_performance_plot():
    # Query all tasks
    tasks = Task.objects.all()
    finished_tasks = FinishedTask.objects.filter(finished=True)

    # Convert queryset to DataFrame
    df_tasks = read_frame(tasks)
    df_finished_tasks = read_frame(finished_tasks)

    # Group tasks by assigned employee and count the number of tasks for each employee
    employee_task_counts = df_tasks['assigned_to'].value_counts()

    # Group finished tasks by assigned employee and count the number of completed tasks for each employee
    employee_finished_task_counts = df_finished_tasks['assigned_to'].value_counts(
    )

    # Merge the two DataFrames on employee name and fill missing values with 0
    df_employee_performance = pd.merge(
        employee_task_counts, employee_finished_task_counts, left_index=True, right_index=True, how='outer').fillna(0)

    # Rename columns for clarity
    df_employee_performance.columns = ['total_tasks', 'completed_tasks']

    # Calculate completion percentage for each employee
    df_employee_performance['completion_percentage'] = (
        df_employee_performance['completed_tasks'] / df_employee_performance['total_tasks']) * 100

    # Sort employees by completion percentage
    df_employee_performance.sort_values(
        by='completion_percentage', ascending=False, inplace=True)

    # Plotting
    plt.figure(figsize=(10, 6))
    sns.barplot(x='completion_percentage', y=df_employee_performance.index,
                data=df_employee_performance, palette='coolwarm')
    plt.title('Employee Performance')
    plt.xlabel('Completion Percentage')
    plt.ylabel('Employee')
    plt.tight_layout()

    # Save the plot
    plt.savefig('ETMDAPP/static/CHARTS/employee_performance.png')
    plt.close()



def generate_task_description_wordcloud():
    tasks = Task.objects.all()
    df_tasks = read_frame(tasks)
    descriptions = ' '.join(df_tasks['description'])

    wordcloud = WordCloud(width=800, height=400,
                          background_color='white').generate(descriptions)

    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title('Task Description Word Cloud')
    plt.tight_layout()
    plt.savefig('ETMDAPP/static/CHARTS/task_description_wordcloud.png')
    plt.close()


def generate_completion_rate_by_employee_plot():
    tasks = Task.objects.all()
    df_tasks = read_frame(tasks)
    total_tasks_by_employee = df_tasks.groupby('assigned_to').size()
    finished_tasks_by_employee = FinishedTask.objects.filter(
        finished=True).values('assigned_to').annotate(count=Count('assigned_to'))

    employee_names = total_tasks_by_employee.index
    completion_rates = []

    for emp in employee_names:
        total_tasks = total_tasks_by_employee.get(emp, 0)
        finished_tasks = next(
            (item['count'] for item in finished_tasks_by_employee if item['assigned_to'] == emp), 0)
        completion_rate = (finished_tasks / total_tasks) * \
            100 if total_tasks > 0 else 0
        completion_rates.append(completion_rate)

    plt.figure(figsize=(8, 8))
    plt.bar(employee_names, completion_rates, color='green')
    plt.title('Task Completion Rate by Employee')
    plt.xlabel('Employee')
    plt.ylabel('Completion Rate (%)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('ETMDAPP/static/CHARTS/completion_rate_by_employee.png')
    plt.close()


def generate_task_distribution_by_category_plot():
    tasks = Task.objects.all()
    df_tasks = read_frame(tasks)
    category_counts = df_tasks['category'].value_counts()

    # Define custom colors for each category
    colors = ['skyblue', 'lightgreen', 'lightcoral', 'orange']

    plt.figure(figsize=(10, 6))
    category_counts.plot(kind='bar', color=colors)
    plt.title('Task Distribution by Category')
    plt.xlabel('Category')
    plt.ylabel('Number of Tasks')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('ETMDAPP/static/CHARTS/task_distribution_by_category.png')
    plt.close()



def generate_task_distribution_by_priority_plot():
    tasks = Task.objects.all()
    df_tasks = read_frame(tasks)
    priority_counts = df_tasks['priority'].value_counts()

    plt.figure(figsize=(10, 6))
    priority_counts.plot(kind='bar', color=['red', 'orange', 'yellow'])
    plt.title('Task Distribution by Priority')
    plt.xlabel('Priority')
    plt.ylabel('Number of Tasks')
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig('ETMDAPP/static/CHARTS/task_distribution_by_priority.png')
    plt.close()

# Function to generate task duration distribution histogram


# Function to generate task duration distribution histogram
# def generate_task_duration_distribution_plot():
#     tasks = Task.objects.all()
#     df_tasks = read_frame(tasks)

#     # Drop rows with null values in deadline_date or created_at columns
#     df_tasks = df_tasks.dropna(subset=['deadline_date', 'created_at'])

#     # Convert deadline_date and created_at columns to datetime if not already
#     df_tasks['deadline_date'] = pd.to_datetime(df_tasks['deadline_date'])
#     df_tasks['created_at'] = pd.to_datetime(df_tasks['created_at'])

#     # Calculate task durations in days
#     task_durations = (df_tasks['deadline_date'] -
#                       df_tasks['created_at']).dt.days

#     plt.figure(figsize=(10, 6))
#     plt.hist(task_durations, bins=20)
#     plt.title('Task Duration Distribution')
#     plt.xlabel('Task Duration (days)')
#     plt.ylabel('Frequency')
#     plt.xticks(rotation=0)
#     plt.tight_layout()
#     plt.savefig('task_duration_distribution.png')
#     plt.close()


