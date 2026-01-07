# Blog/wsgi.py
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Blog.settings')

application = get_wsgi_application()

# 👇 THIS IS REQUIRED FOR VERCEL
app = application