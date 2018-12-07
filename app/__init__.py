import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os
from flask import Flask, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_security import Security, SQLAlchemyUserDatastore, current_user
from flask_admin import Admin
from flask_mail import Mail
import flask_excel as excel
from config import Config
from sqlalchemy import event
from elasticsearch import Elasticsearch
import logging
from logging.handlers import SMTPHandler
from geopy.geocoders import Nominatim
from redis import Redis
from flask_dance.contrib.azure import make_azure_blueprint
from flask_dance.contrib.facebook import make_facebook_blueprint
from flask_dance.contrib.dropbox import make_dropbox_blueprint
from flask_dance.consumer.backend.sqla import SQLAlchemyBackend
from werkzeug.contrib.fixers import ProxyFix
from flask_dance.consumer import OAuth2ConsumerBlueprint
from flask_dance.consumer import oauth_authorized
from elasticsearch import Elasticsearch
import rq

app = Flask(__name__)
db = SQLAlchemy()
migrate = Migrate()
security = Security()
admin = Admin()
mail = Mail()
geolocator = Nominatim(user_agent='Assignably')

def create_app(config_class=Config):
        app = Flask(__name__)
        app.wsgi_app = ProxyFix(app.wsgi_app)
        app.config.from_object(config_class)
        app.redis = Redis.from_url(app.config['REDIS_URL'])
        app.task_queue = rq.Queue('assignably-tasks', connection=app.redis)
        app.elasticsearch = Elasticsearch([app.config['ELASTICSEARCH_URL']]) \
            if app.config['ELASTICSEARCH_URL'] else None

        if not app.debug:
            from flask_sslify import SSLify
            sslify = SSLify(app)
        
        db.init_app(app)
        migrate.init_app(app, db)
        mail.init_app(app)
        excel.init_excel(app)


        from app.models.role import Role
        from app.models.user import User

        user_datastore = SQLAlchemyUserDatastore(db, User, Role)
        security.init_app(app=app, datastore=user_datastore)

        from app.views import *#dashboard_bp, errors_bp, upload_bp, marketing_bp
        app.register_blueprint(dashboard_bp)
        app.register_blueprint(errors_bp)
        app.register_blueprint(upload_bp, url_prefix="/import")
        app.register_blueprint(marketing_bp, url_prefix="/marketing")

        from app.admin import create_admin
        admin = create_admin(app, db)

        if not app.debug and not app.testing:
            if app.config['LOG_TO_STDOUT']:
                stream_handler = logging.StreamHandler()
                stream_handler.setLevel(logging.INFO)
                app.logger.addHandler(stream_handler)
            else:
                if not os.path.exists('logs'):
                    os.mkdir('logs')
                file_handler = RotatingFileHandler('logs/assignably.log',
                                                   maxBytes=10240, backupCount=10)
                file_handler.setFormatter(logging.Formatter(
                    '%(asctime)s %(levelname)s: %(message)s '
                    '[in %(pathname)s:%(lineno)d]'))
                file_handler.setLevel(logging.INFO)
                app.logger.addHandler(file_handler)

            app.logger.setLevel(logging.INFO)
            app.logger.info('Assignably startup')

        return app

#from app.models.role import Role
#from app.models.user import User
#from app.models.task import Task
#from app.models.address import Address
#from app.models.contact import Contact
