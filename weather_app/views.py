from celery.schedules import crontab
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView

from weather_app.models import Weather
from weather_app.serializers import WeatherSerializer, TaskScheduleSerializer
from weather_project.celery import app


class WeatherViewSet(viewsets.ModelViewSet):
    queryset = Weather.objects.all()
    serializer_class = WeatherSerializer


class TaskScheduleView(APIView):
    def post(self, request):
        serializer = TaskScheduleSerializer(data=request.data)
        if serializer.is_valid():
            schedule = serializer.validated_data
            hour = schedule.get("hour")
            minute = schedule.get("minute")

            # Оновлення розкладу задачі через Celery Beat
            app.conf.beat_schedule["run-every-day-at-9am"]["schedule"] = crontab(
                hour=hour, minute=minute
            )

            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
