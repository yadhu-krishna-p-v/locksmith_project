import os
from celery import Celery
from celery.schedules import crontab

# Set default Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "locksmith_project.settings")

celery_app = Celery("locksmith_project")

# Load task modules from all registered Django app configs.
celery_app.config_from_object("django.conf:settings", namespace="CELERY")
celery_app.autodiscover_tasks()

celery_app.conf.beat_schedule.update({
    "process_payouts": {
        "task": "payments.tasks.process_payouts",
        "schedule": crontab(hour=2, minute=0),  # Runs daily at 2 AM
    },
})
