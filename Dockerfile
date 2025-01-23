# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code into the container
COPY . .

# Set environment variables for Django
ENV DJANGO_SETTINGS_MODULE=dashboard_project.settings
ENV PYTHONPATH=/app/dashboard_project

# Start the Gunicorn server
CMD ["gunicorn", "dashboard_project.wsgi:application", "--bind", "0.0.0.0:$PORT"]
