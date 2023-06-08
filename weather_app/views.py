from django_celery_beat.models import PeriodicTask
from rest_framework import viewsets, status
from rest_framework.response import Response

from weather_app.models import Weather
from weather_app.serializers import WeatherSerializer, TaskScheduleSerializer


class WeatherViewSet(viewsets.ModelViewSet):
    queryset = Weather.objects.all()
    serializer_class = WeatherSerializer


class TaskScheduleViewSet(viewsets.ViewSet):
    def list(self, request):
        try:
            task = PeriodicTask.objects.get(name='run-every-day-at-9am')
        except PeriodicTask.DoesNotExist:
            return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = TaskScheduleSerializer(instance=task)
        return Response(serializer.data)

    def create(self, request):
        try:
            task = PeriodicTask.objects.get(name='run-every-day-at-9am')
            serializer = TaskScheduleSerializer(instance=task, data=request.data)
        except PeriodicTask.DoesNotExist:
            serializer = TaskScheduleSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Task schedule created'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        try:
            task = PeriodicTask.objects.get(name='run-every-day-at-9am')
        except PeriodicTask.DoesNotExist:
            return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = TaskScheduleSerializer(instance=task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Task schedule updated'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)