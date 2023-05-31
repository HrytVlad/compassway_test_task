from celery.schedules import crontab

from .parser import parse_weather

from celery import shared_task, Celery

from weather_project.celery import app


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(crontab(minute=1))


#
# @shared_task
# def run_parse_weather():
#     parse_weather()
@app.task
def test(*args, **kwargs):
    print("Hello")
