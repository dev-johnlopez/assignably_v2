from rq import get_current_job
import sys
from app import create_app
from app import db
from app.models.task import Task
from app.models.user import User
from app.src.upload import validDataFrame, listsource_headers, processRow
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
        task.user.add_notification('task_progress', {'task_id': job.get_id(),
                                                     'progress': progress})
        if progress >= 100:
            task.complete = True
        db.session.commit()

def import_leads(user_id, data_frame):
    try:
        job = get_current_job()
        task = Task.query.get(job.get_id())
        user = task.user
        g.user = user
        if validDataFrame(data_frame, listsource_headers):
            _set_task_progress(0)
            total_rows = len(data_frame.index)
            for index, row in data_frame.iterrows():
                processRow(row)
                _set_task_progress(100 * (index + 1) // total_rows)
            user.add_notification('bulk_upload_complete', None)
            db.session.commit()
            _set_task_progress(100)
    except:
        _set_task_progress(100)
        app.logger.error('Unhandled exception', exc_info=sys.exc_info())
