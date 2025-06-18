from django.utils import timezone
from .models import Job
import logging
from cron_validator import CronValidator
from datetime import datetime

logger = logging.getLogger(__name__)

def execute_job(job_id):
    try:
        job = Job.objects.get(id=job_id)
        logger.info(f"Executing job: {job.name} with parameters: {job.parameters}")
        
        # Update job timestamps
        job.last_run = timezone.now()
        job.next_run = calculate_next_run(job)
        job.save()
        
        if job.parameters.get('action') == 'send_email':
            logger.info(f"Sending email notification for job {job.name}")
        elif job.parameters.get('action') == 'something_else':
            logger.info(f"Performing number crunching for job {job.name}")
            
    except Job.DoesNotExist:
        logger.error(f"Job with ID {job_id} not found")
    except Exception as e:
        logger.error(f"Error executing job {job_id}: {str(e)}")

def calculate_next_run(job):
    try:
        # Use cron-validator to get the next scheduled time
        schedule = CronValidator.get_schedule(job.cron_expression, job.last_run or job.start_time)
        return schedule.next()
    except Exception as e:
        logger.error(f"Error calculating next run for job {job.id}: {str(e)}")
        return None
