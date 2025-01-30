import os
from celery import Celery

# Set default Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "locksmith_project.settings")

celery_app = Celery("locksmith_project")

# Load task modules from all registered Django app configs.
celery_app.config_from_object("django.conf:settings", namespace="CELERY")
celery_app.autodiscover_tasks()
