from celery import Celery
from app.database import SessionLocal
from app.models import AccessLog
from datetime import datetime

celery_app = Celery('tasks', broker='redis://localhost:6379/0')

@celery_app.task
def log_access(log_text):
    db = SessionLocal()
    try:
        access_log = AccessLog(text=log_text)
        db.add(access_log)
        db.commit()
    except Exception as e:
        print(f"Error logging access: {e}")
    finally:
        db.close()