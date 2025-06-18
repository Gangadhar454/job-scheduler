from rest_framework import serializers
from .models import Job
from cron_validator import CronValidator

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = [
            'id',
            'name',
            'description',
            'cron_expression',
            'start_time',
            'last_run',
            'next_run',
            'parameters',
            'is_active',
            'created_at', 
            'updated_at'
        ]

    def validate_cron_expression(self, value):
        try:
            CronValidator.parse(value)
        except ValueError as e:
            raise serializers.ValidationError(f"Invalid CRON expression: {str(e)}")
        return value