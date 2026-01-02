# Dockerfile
FROM python:3.11-slim

# Prevent Python from writing pyc files to disc
ENV PYTHONDONTWRITEBYTECODE 1
# Prevent Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED 1

# Install system dependencies (needed for Postgres client)
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user
RUN useradd -m django_user

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Chown all the files to the app user
RUN chown -R django_user:django_user /app

# Switch to non-root user
USER django_user

# Expose the port
EXPOSE 8000

# Command to run the application (Adjust 'blog_project' to your actual project name)
# We use gunicorn for production-grade serving, standard implementation requires installing it
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "blog_project.wsgi:application"]