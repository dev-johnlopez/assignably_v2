from rq import get_current_job
from app import create_app
from app import db
from app.models.task import Task
from app.models.user import User
from app.src.upload import upload_lead_dataframe
from flask import current_app, g
from flask_security import current_user

app = create_app()
app.app_context().push()

def _set_task_progress(progress):
    job = get_current_job()
    if job:
        job.meta['progress'] = progress
        job.save_meta()
        task = Task.query.get(job.get_id())
        #task.user.add_notification('task_progress', {'task_id': job.get_id(),
        #                                             'progress': progress})
        if progress >= 100:
            task.complete = True
        db.session.commit()

def import_leads(user_id, data_frame):
    job = get_current_job()
    task = Task.query.get(job.get_id())
    user = task.user
    print("*****")
    print("*****")
    print("*****")
    print("*****")
    print("*****")
    print("*****")
    print("*****")
    print("*****")
    print("*****")
    print(current_user)
    g.user = user
    print(g.user)
    #current_app.security.login_user(user)
    upload_lead_dataframe(data_frame, user)
