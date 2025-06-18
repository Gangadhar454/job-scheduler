from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from django.utils import timezone
from .models import Job
from .tasks import execute_job
import logging

logger = logging.getLogger(__name__)

class JobScheduler:
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.scheduler.start()

    def schedule_job(self, job):
        if not job.is_active:
            return

        trigger = CronTrigger.from_crontab(job.cron_expression,)
        self.scheduler.add_job(
            execute_job,
            trigger=trigger,
            id=str(job.id),
            name=job.name,
            kwargs={'job_id': job.id},
            start_date=job.start_time
        )
        logger.info(f"Scheduled job {job.name} with ID {job.id} using CRON {job.cron_expression}")

    def remove_job(self, job_id):
        try:
            self.scheduler.remove_job(str(job_id))
            logger.info(f"Removed job with ID {job_id}")
        except Exception as e:
            logger.error(f"Error removing job {job_id}: {str(e)}")

    def reschedule_all_jobs(self):
        self.scheduler.remove_all_jobs()
        for job in Job.objects.filter(is_active=True):
            self.schedule_job(job)