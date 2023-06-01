import os

from celery import Celery
from celery.schedules import crontab

from weather_project import settings

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "weather_project.settings")

app = Celery("weather_project")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django apps.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.conf.beat_schedule = {
    "run-every-day-at-9am": {
        "task": "weather_app.tasks.run_parse_weather",
        "schedule": crontab(minute=0, hour=9),
    },
}


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
