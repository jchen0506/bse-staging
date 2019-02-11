"""Flask app configuration
"""
import os
import basis_set_exchange as bse


class BaseConfig:

    basedir = os.path.abspath(os.path.dirname(__file__))
    # STATIC_FOLDER = 'static'
    ADMINS = frozenset(['daltarawy@molssi.org'])
    SECRET_KEY = os.environ.get('SECRET_KEY', 'SecretKeyForSessionSigning')

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
    APP_ADMIN = os.environ.get('APP_ADMIN', 'daltarawy@vt.edu')
    EMAIL_CONFIRMATION_ENABLED = False

    # Client-side config
    OLD_VERSION_SELECTION_STYLE = False

    # Version of the BSE library
    BSE_LIBRARY_VERSION = bse.version()


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    TESTING = False
    DB_LOGGING = True
    MONGODB_SETTINGS = {
        'host': os.environ.get('MONGO_URI',
                               "mongodb://user:pass@ds131905.mlab.com:31905/bse_staging"),  # URI
    }


class TestingConfig(BaseConfig):
    DEBUG = False
    TESTING = True
    DB_LOGGING = True
    EMAIL_CONFIRMATION_ENABLED = True
    # disable CSRF protection in testing
    WTF_CSRF_ENABLED = False
    MONGODB_SETTINGS = {
        'db': "test_bse_db",
        # 'username': 'travis',
        # 'password': 'test'
    }


class ProductionConfig(BaseConfig):
    DEBUG = False
    TESTING = False
    DB_LOGGING = True
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
