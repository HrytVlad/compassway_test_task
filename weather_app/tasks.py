from .parser import parse_weather


from weather_project.celery import app


@app.task()
def run_parse_weather():
    parse_weather()
