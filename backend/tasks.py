from datetime import datetime, timedelta

from celery_app import celery
from database import db
from models.application import Application
from models.notification import Notification


@celery.task
def interview_reminder_task():
    now = datetime.now()
    reminder_limit = now + timedelta(hours=24)

    applications = Application.query.filter(
        Application.interview_date.isnot(None),
        Application.interview_time.isnot(None),
        Application.status == "Interview"
    ).all()

    reminders_created = 0

    for application in applications:
        interview_datetime = datetime.combine(
            application.interview_date,
            application.interview_time
        )

        # Only remind about interviews happening in the next 24 hours
        if now <= interview_datetime <= reminder_limit:

            title = "Interview Reminder"

            message = (
                f"You have an interview scheduled on "
                f"{application.interview_date} at "
                f"{application.interview_time}."
            )

            if application.interview_location:
                message += (
                    f" Location: {application.interview_location}."
                )

            # Prevent duplicate reminders
            existing_notification = Notification.query.filter_by(
                student_id=application.student_id,
                title=title,
                message=message
            ).first()

            if not existing_notification:
                notification = Notification(
                    student_id=application.student_id,
                    title=title,
                    message=message
                )

                db.session.add(notification)
                reminders_created += 1

    db.session.commit()

    print(f"Interview reminders created: {reminders_created}")

    return {
        "reminders_created": reminders_created
    }