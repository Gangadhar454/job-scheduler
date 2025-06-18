from django.apps import AppConfig
import sys

class JobsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'jobs'

    def ready(self):
        if 'migrate' not in sys.argv and 'makemigrations' not in sys.argv:
            from .services import JobScheduler
            scheduler = JobScheduler()
            scheduler.reschedule_all_jobs()