from fastapi import HTTPException, BackgroundTasks
from email_validator import validate_email, EmailNotValidError
from datetime import datetime

# -----------------------------
# Validate Email
# -----------------------------
def validate_user_email(email: str):
    try:
        validate_email(email)
        return True
    except EmailNotValidError:
        raise HTTPException(400, "Invalid email format")


# -----------------------------
# Dummy Email Reminder
# -----------------------------
def send_reminder_email(email: str, task_title: str):
    """
    This function simulates sending an email.
    In production, connect with SMTP / SendGrid / Mailgun.
    """
    print(f"[REMINDER EMAIL] To: {email} | Task: {task_title}")


def schedule_reminder(background_tasks: BackgroundTasks, email: str, task_title: str):
    """Background task wrapper."""
    background_tasks.add_task(send_reminder_email, email, task_title)


# -----------------------------
# Extract Bearer Token
# -----------------------------
def extract_token(auth_header: str):
    """
    Extracts token from a string like: "Bearer <token>"
    """
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(401, "Invalid authorization header")

    return auth_header.split(" ")[1]


# -----------------------------
# Create Timestamp
# -----------------------------
def current_timestamp():
    return datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")


# -----------------------------
# Clean dict (remove None values)
# -----------------------------
def clean_dict(data: dict):
    """
    Removes keys where value is None.
    Useful for update operations.
    """
    return {k: v for k, v in data.items() if v is not None}
