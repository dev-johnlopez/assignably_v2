from flask import Blueprint

dashboard_bp = Blueprint('dashboard', __name__)

from . import dashboard

errors_bp = Blueprint('errors', __name__)

from . import errors

upload_bp = Blueprint('upload', __name__)

from . import upload

marketing_bp = Blueprint('marketing', __name__)

from . import marketing

leads_bp = Blueprint('leads', __name__)

from . import leads

deals_bp = Blueprint('deals', __name__)

from . import deals

proformas_bp = Blueprint('proformas', __name__)

from . import proformas

markets_bp = Blueprint('markets', __name__)

from . import markets
