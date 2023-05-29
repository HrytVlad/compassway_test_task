from rest_framework import viewsets

from weather_app.models import Weather
from weather_app.serializers import WeatherSerializer


class WeatherViewSet(viewsets.ModelViewSet):
    queryset = Weather.objects.all()
    serializer_class = WeatherSerializer
