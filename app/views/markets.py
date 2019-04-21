from flask import g, render_template, jsonify, json, request
from app import db
from app.views import markets_bp as bp
from app.forms.search import SearchForm
from app.forms.markets import RegionForm
from flask_security import current_user, login_required
from app.models.market import *
from app.constants import dataset as DATASET_CONSTANTS
import json
#from app.crm.models import Contact

@bp.before_app_request
def before_request():
    g.search_form = SearchForm()

@bp.route('/')
@login_required
def index():
    data_sets = [{'name': DATASET_CONSTANTS.DATASET_TYPE[r.type], 'type': r.type} for r in db.session.query(DataPoint.type).distinct()]
    return render_template('markets/index.html',
                title='Market Data',
                data_sets=data_sets)

@bp.route('view/<market_id>')
@login_required
def view(market_id):
    market = Market.query.get_or_404(market_id)
    return render_template('markets/view.html',
                title='View Market',
                market=market)

@bp.route('/dataset/<dataset_type>')
@login_required
def dataset(dataset_type):
    form = RegionForm()
    markets = Market.query.filter_by(region_type=0, region_id=102001).all()
    max_year = db.session.query(db.func.max(DataPoint.year)).scalar()
    max_month = db.session.query(db.func.max(DataPoint.month)).scalar()
    top_markets = DataPoint.query.filter_by(year=max_year, month=max_month, type=dataset_type).order_by(DataPoint.value).all()
    return render_template('markets/dataset.html',
                title='Market Data',
                dataset_type = dataset_type,
                markets=markets,
                top_markets=top_markets,
                form=form)

@bp.route('/get/region_data')
def getMarket():
    region_id = int(request.args.get('region_id'))
    data_record = Market.query.filter_by(region_id=region_id).first_or_404()
    return jsonify(data_record.serialize)

@bp.route('/regions', methods=['GET'])
def regions():
    region_type = int(request.args.get('region_type'))
    region_name = request.args.get('region_name')
    regions = Market.query.filter_by(region_type=region_type)

    regionArray = []
    for region in regions:
        regionObj = {}
        regionObj['id'] = region.region_id
        regionObj['name'] = region.region_name
        regionArray.append(regionObj)

    regionArray.sort(key=lambda region: region['name'])

    return jsonify({'regions' : regionArray})
