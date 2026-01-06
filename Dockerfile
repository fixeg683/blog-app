FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Create static files directory
RUN mkdir -p /app/staticfiles
RUN SECRET_KEY=building_static_files python manage.py collectstatic --noinput

# 👇 NEW: Copy the entrypoint script and make it executable
COPY docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

EXPOSE 10000

# 👇 CHANGED: Use the script as the default command
CMD ["docker-entrypoint.sh"]