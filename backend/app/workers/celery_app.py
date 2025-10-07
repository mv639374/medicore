# What: The main configuration file for Celery. It tells Celery how to connect to our Redis server (which acts as the "message broker" to queue tasks) and automatically discover our task files.

# Why: This is the central entry point for our entire asynchronous processing system.

from celery import Celery
from app.config import settings

# Initialize Celery
celery_app = Celery(
    'medicore_tasks',
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=['app.workers.tasks.diagnostic'] # Explicitly include tasks module
)

# Celery configuration
celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    task_track_started=True,
    worker_prefetch_multiplier=1,
)