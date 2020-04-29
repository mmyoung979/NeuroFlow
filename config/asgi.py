"""
ASGI config for neuroflow project.
It exposes the ASGI callable as a module-level variable named ``application``.
"""
# Django imports
from django.core.asgi import get_asgi_application

# Python imports
import os


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'neuroflow.settings')
application = get_asgi_application()
