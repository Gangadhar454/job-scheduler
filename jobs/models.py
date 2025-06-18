from django.db import models

class Job(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    cron_expression = models.CharField(max_length=100)
    start_time = models.DateTimeField()
    last_run = models.DateTimeField(null=True, blank=True)
    next_run = models.DateTimeField(null=True, blank=True)
    parameters = models.JSONField(default=dict)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        indexes = [
            models.Index(fields=['next_run']),
            models.Index(fields=['is_active']),
        ]