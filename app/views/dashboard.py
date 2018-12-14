from flask import g, render_template, flash, redirect, url_for, request, current_app
from app import db
from app.views import dashboard_bp as bp
from app.forms.search import SearchForm
from flask_security import current_user, login_required
from app.models.contact import Contact
#from app.crm.models import Contact

@bp.before_app_request
def before_request():
    g.search_form = SearchForm()

@bp.route('/')
@login_required
def index():
    contact_leads = current_user.get_contact_leads()
    property_leads = current_user.get_property_leads()
    return render_template('main/index.html',
                title='Dashboard',
                contact_leads=len(contact_leads),
                property_leads=len(property_leads))

@bp.route('/search', methods=['GET'])
@login_required
def search():
    if not g.search_form.validate():
        return redirect(url_for('dashboard.index'))
    page = request.args.get('page', 1, type=int)
    contacts, total = Contact.search(g.search_form.q.data, page,
                               current_app.config['POSTS_PER_PAGE'])
    next_url = url_for('dashboard.search', q=g.search_form.q.data, page=page + 1) \
        if total > page * current_app.config['POSTS_PER_PAGE'] else None
    prev_url = url_for('dashboard.search', q=g.search_form.q.data, page=page - 1) \
        if page > 1 else None
    return render_template('main/search.html', title='Search', contacts=contacts,
                           next_url=next_url, prev_url=prev_url)

@bp.route('/log_call', methods=['GET', 'POST'])
@login_required
def log_call():
    return render_template('main/log_call.html', title='Log Call')

@bp.route('/notifications')
@login_required
def notifications():
    since = request.args.get('since', 0.0, type=float)
    notifications = current_user.notifications.filter(
        Notification.timestamp > since).order_by(Notification.timestamp.asc())
    return jsonify([{
        'name': n.name,
        'data': n.get_data(),
        'timestamp': n.timestamp
    } for n in notifications])
