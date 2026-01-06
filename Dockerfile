# 1. Use an official Python runtime as a parent image
FROM python:3.11-slim

# 2. Set environment variables
# Prevent Python from writing pyc files to disc
ENV PYTHONDONTWRITEBYTECODE 1
# Prevent Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED 1

# 3. Set the working directory in the container
WORKDIR /app

# 4. Install dependencies
# We copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the project code into the container
COPY . .

# 6. FIX: Create the staticfiles directory and generate files
# We pass a dummy SECRET_KEY here to prevent Django from crashing during the build
RUN mkdir -p /app/staticfiles
RUN SECRET_KEY=building_static_files python manage.py collectstatic --noinput

# 7. Expose the port (Documenting that this container listens on 8000)
EXPOSE 8000

# 8. Define the default start command
# This connects Gunicorn to your 'Blog' folder
CMD ["gunicorn", "Blog.wsgi:application", "--bind", "0.0.0.0:8000"]