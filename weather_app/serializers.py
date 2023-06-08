from django_celery_beat.models import PeriodicTask, CrontabSchedule
from rest_framework import serializers

from weather_app.models import Weather


class WeatherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Weather
        fields = "__all__"


class CrontabScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrontabSchedule
        fields = ("minute", "hour")


class TaskScheduleSerializer(serializers.ModelSerializer):
    crontab = CrontabScheduleSerializer()

    class Meta:
        model = PeriodicTask
        fields = ("name", "crontab", "enabled", "last_run_at", "total_run_count")

    def update(self, instance, validated_data):
        crontab_data = validated_data.pop("crontab", None)
        if crontab_data:
            instance.crontab.minute = crontab_data.get(
                "minute", instance.crontab.minute
            )
            instance.crontab.hour = crontab_data.get("hour", instance.crontab.hour)
            instance.crontab.save()

        return super().update(instance, validated_data)
