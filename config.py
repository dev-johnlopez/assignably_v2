import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.flaskenv'))

class Config(object):
    DEBUG = os.environ.get('FLASK_DEBUG') or False
    ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL')
    POSTS_PER_PAGE = int(os.environ.get('POSTS_PER_PAGE'))
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')
    SECURITY_REGISTERABLE = int(os.environ.get('SECURITY_REGISTERABLE'))
    SECURITY_RECOVERABLE = int(os.environ.get('SECURITY_RECOVERABLE'))
    SECURITY_PASSWORD_SALT = os.environ.get('SECURITY_PASSWORD_SALT')
    SECURITY_EMAIL_SENDER = os.environ.get('SECURITY_EMAIL_SENDER')
    SECURITY_FLASH_MESSAGES = True
    SEND_REGISTER_EMAIL = int(os.environ.get('SEND_REGISTER_EMAIL'))
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')
    ADMINS = ['john@johnlopez.org']
    REDIS_URL = os.environ.get('REDIS_URL') or 'redis://'
    SECURITY_TRACKABLE = True
    AZURE_OAUTH_CLIENT_ID = os.environ.get('AZURE_OAUTH_CLIENT_ID')
    AZURE_OAUTH_CLIENT_SECRET = os.environ.get('AZURE_OAUTH_CLIENT_SECRET')
    FACEBOOK_OAUTH_CLIENT_ID = os.environ.get('FACEBOOK_OAUTH_CLIENT_ID')
    FACEBOOK_OAUTH_CLIENT_SECRET = os.environ.get('FACEBOOK_OAUTH_CLIENT_SECRET')
    DROPBOX_OAUTH_APP_KEY = os.environ.get('DROPBOX_OAUTH_APP_KEY')
    DROPBOX_OAUTH_APP_SECRET= os.environ.get('DROPBOX_OAUTH_APP_SECRET')
