"""Flask app configuration
"""
import os


class BaseConfig:

    basedir = os.path.abspath(os.path.dirname(__file__))
    # STATIC_FOLDER = 'static'
    ADMINS = frozenset(['daltarawy@molssi.org'])
    SECRET_KEY = os.environ.get('SECRET_KEY', 'SecretKeyForSessionSigning')

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')

    THREADS_PER_PAGE = 8


    # email
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.googlemail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', '587'))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in \
        ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME', 'user')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD', 'pass')
    MAIL_SUBJECT_PREFIX = '[MolSSI CMS Software DB]'
    MAIL_SENDER = 'BSE Website <info@molssi.org>'
    APP_ADMIN = os.environ.get('APP_ADMIN', 'admin@molssi.org')
    EMAIL_CONFIRMATION_ENABLED = False

    # Client-side config
    OLD_VERSION_SELECTION_STYLE = False


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    TESTING = False
    MONGODB_SETTINGS = {
        'host': os.environ.get('MONGO_URI',
                               "mongodb://<user>:<dbpassword>@ds14323111.mlab.com:43231/bse_logging"),  # URI
    }


class TestingConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    MONGODB_SETTINGS = {
        'host': os.environ.get('MONGO_URI',
                               "mongodb://<user>:<dbpassword>@ds14323111.mlab.com:43231/bse_logging")
    }


class ProductionConfig(BaseConfig):
    DEBUG = False
    TESTING = False
    MONGODB_SETTINGS = {
        'host': os.environ.get('MONGO_URI',
                               "mongodb://<user>:<dbpassword>@ds14323111.mlab.com:43231/bse_logging"),
    }


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    # 'docker': DockerConfig,

    'default': DevelopmentConfig
}