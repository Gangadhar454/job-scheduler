from django.contrib import admin
from .models import Job

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('name', 'cron_expression', 'next_run', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'description', 'cron_expression')