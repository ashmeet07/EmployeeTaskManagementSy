# Use the official Python image as the base
FROM python:3.13.2

# Set the working directory inside the container
WORKDIR /app

# Copy all files into the container
COPY . /app/

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Expose the Django default port
EXPOSE 8000

# Command to start Django server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
