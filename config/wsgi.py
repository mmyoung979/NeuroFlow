"""
WSGI config for neuroflow project.
It exposes the WSGI callable as a module-level variable named ``application``.
"""
# Django imports
from django.core.wsgi import get_wsgi_application

# Python imports
import os


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'neuroflow.settings')
application = get_wsgi_application()
