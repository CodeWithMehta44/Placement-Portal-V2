from datetime import datetime, timedelta,date

import os
import csv

from celery_app import celery
from database import db
from models.application import Application
from models.notification import Notification
from models.placement import Placement
from models.student import Student
from models.company import Company
from models.job_position import JobPosition



@celery.task
def export_applications_csv_task():
    """
    Generate CSV file containing application history.
    """

    exports_dir = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "exports"
    )

    os.makedirs(exports_dir, exist_ok=True)

    export_file = os.path.join(
        exports_dir,
        "application_history.csv"
    )

    applications = Application.query.all()

    with open(export_file, "w", newline="", encoding="utf-8") as file:

        writer = csv.writer(file)

        # CSV header
        writer.writerow([
            "Application ID",
            "Student ID",
            "Company ID",
            "Status",
            "Interview Date",
            "Interview Time",
            "Interview Location",
            "Applied Date"
        ])

        for application in applications:
            job = JobPosition.query.get(application.job_id)
            company_id = job.company_id if job else None

            writer.writerow([
                application.id,
                application.student_id,
                company_id,
                application.status,
                application.interview_date,
                application.interview_time,
                application.interview_location,
                application.applied_date
            ])

    print(f"Application CSV generated: {export_file}")

    return {
        "file": export_file,
        "records": len(applications)
    }

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


@celery.task
def monthly_placement_report_task(year=None, month=None):
    """
    Generate a monthly placement report.
    """

    now = datetime.now()

    if year is None:
        year = now.year

    if month is None:
        month = now.month

    # Start of selected month
    start_date = date(year, month, 1)

    # Start of next month
    if month == 12:
        end_date = date(year + 1, 1, 1)
    else:
        end_date = date(year, month + 1, 1)

    # Get placements for selected month
    placements = Placement.query.filter(
        Placement.joining_date >= start_date,
        Placement.joining_date < end_date
    ).all()

    # Overall statistics
    total_students = Student.query.count()
    total_companies = Company.query.count()

    # Company-wise placement count
    company_counts = {}

    placement_rows = []

    for placement in placements:

        student = Student.query.get(placement.student_id)
        company = Company.query.get(placement.company_id)

        company_name = (
            company.company_name
            if company
            else "Unknown Company"
        )

        student_name = (
            student.full_name
            if student
            else "Unknown Student"
        )

        company_counts[company_name] = (
            company_counts.get(company_name, 0) + 1
        )

        placement_rows.append({
            "student": student_name,
            "company": company_name,
            "position": placement.position,
            "salary": placement.salary,
            "joining_date": placement.joining_date
        })

    # Average salary
    salaries = [
        p.salary
        for p in placements
        if p.salary is not None
    ]

    average_salary = (
        sum(salaries) / len(salaries)
        if salaries
        else 0
    )

    # Create reports directory
    reports_dir = os.path.join(
        os.path.dirname(__file__),
        "reports"
    )

    os.makedirs(reports_dir, exist_ok=True)

    report_file = os.path.join(
        reports_dir,
        f"placement_report_{year}_{month:02d}.html"
    )

    # Generate HTML
    html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">

    <title>
        Placement Report - {month:02d}/{year}
    </title>

    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 40px;
        }}

        h1 {{
            text-align: center;
        }}

        .stats {{
            display: flex;
            gap: 20px;
            margin: 30px 0;
        }}

        .card {{
            border: 1px solid #ccc;
            padding: 20px;
            flex: 1;
            text-align: center;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }}

        th, td {{
            border: 1px solid #ccc;
            padding: 10px;
            text-align: left;
        }}

        th {{
            background: #f2f2f2;
        }}
    </style>
</head>

<body>

    <h1>Placement Report</h1>

    <h2>
        {month:02d}/{year}
    </h2>

    <div class="stats">

        <div class="card">
            <h3>Total Students</h3>
            <p>{total_students}</p>
        </div>

        <div class="card">
            <h3>Total Companies</h3>
            <p>{total_companies}</p>
        </div>

        <div class="card">
            <h3>Placements</h3>
            <p>{len(placements)}</p>
        </div>

        <div class="card">
            <h3>Average Salary</h3>
            <p>₹{average_salary:,.2f}</p>
        </div>

    </div>

    <h2>Placement Details</h2>

    <table>

        <tr>
            <th>Student</th>
            <th>Company</th>
            <th>Position</th>
            <th>Salary</th>
            <th>Joining Date</th>
        </tr>
"""

    for row in placement_rows:

        html += f"""
        <tr>
            <td>{row['student']}</td>
            <td>{row['company']}</td>
            <td>{row['position']}</td>
            <td>₹{row['salary']:,.2f}</td>
            <td>{row['joining_date']}</td>
        </tr>
"""

    html += """
    </table>

    <h2>Company-wise Placements</h2>

    <table>

        <tr>
            <th>Company</th>
            <th>Placements</th>
        </tr>
"""

    for company, count in company_counts.items():

        html += f"""
        <tr>
            <td>{company}</td>
            <td>{count}</td>
        </tr>
"""

    html += """
    </table>

</body>
</html>
"""

    with open(report_file, "w", encoding="utf-8") as file:
        file.write(html)

    print(f"Placement report generated: {report_file}")

    return {
        "report_file": report_file,
        "placements": len(placements),
        "average_salary": average_salary
    }