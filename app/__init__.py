from flask import Flask
from config import config
from flask_mongoengine import MongoEngine
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from flask_admin import Admin
from flask_login import LoginManager
from flask_moment import Moment


mail = Mail()
db = MongoEngine()
bootstrap = Bootstrap()
moment = Moment()
app_admin = Admin(name='BSE Logging Admin', template_mode='bootstrap3',
                  base_template='admin/custom_base.html')

login_manager = LoginManager()
login_manager.login_view = 'auth.login'   # endpoint name for the login view


def create_app(config_name):
    """Flask app factory pattern
       separately creating the extensions and later initializing"""

    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # init
    mail.init_app(app)
    db.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)
    login_manager.init_app(app)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # create user roles
    from .models.users import update_roles
    update_roles()

    # To avoid circular import
    from app.admin import add_admin_views
    add_admin_views()

    # Then init the app
    app_admin.init_app(app)

    return app

