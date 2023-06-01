from celery.schedules import crontab
from rest_framework import serializers

from weather_app.models import Weather


class WeatherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Weather
        fields = "__all__"


class TaskScheduleSerializer(serializers.Serializer):
    hour = serializers.IntegerField(min_value=0, max_value=23)
    minute = serializers.IntegerField(min_value=0, max_value=59)

    def validate(self, attrs):
        hour = attrs.get("hour")
        minute = attrs.get("minute")
        if hour is not None and minute is not None:
            crontab(hour=hour, minute=minute)
        return attrs
