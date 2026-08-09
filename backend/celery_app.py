from celery import Celery
from celery.schedules import crontab
from app import app


celery = Celery(
    "placement_portal",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0",
    include=["tasks"]
)


celery.conf.update(
    timezone="Asia/Kolkata",
    enable_utc=False,
    beat_schedule={
        "check-interview-reminders": {
            "task": "tasks.interview_reminder_task",
            "schedule": crontab(minute="0"),
        },
    },
)


class FlaskTask(celery.Task):
    def __call__(self, *args, **kwargs):
        with app.app_context():
            return self.run(*args, **kwargs)


celery.Task = FlaskTask