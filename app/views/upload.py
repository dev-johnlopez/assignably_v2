from flask import g, render_template, flash, redirect, url_for, request
from flask_security import current_user
from app import db
from app.views import upload_bp as bp
from app.forms.upload import UploadForm
from app.src.upload import readExcel
from app.forms.search import SearchForm
#from app.src.util.excel.excel_import import ExcelReader
from flask_security import login_required

@bp.before_app_request
def before_request():
    g.search_form = SearchForm()

@bp.route('/', methods=['GET','POST'])
@login_required
def index():
    form = UploadForm()
    if form.validate_on_submit():
        data_frame = readExcel(form.file.data, current_user)
        current_user.launch_task('import_leads', 'Importing Leads', user_id=current_user.id, data_frame=data_frame)
        #upload_leads(form.file.data, current_user)
        db.session.commit()
    return render_template('upload/index.html', title='Upload', form=form)
