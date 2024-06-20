from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_bootstrap import Bootstrap5
from flask_mail import Mail
from config import config
from flask_login import LoginManager
from flask_admin import Admin
from authlib.integrations.flask_client import OAuth

bootstrap = Bootstrap5()
db = SQLAlchemy()
mail = Mail()
login_manager = LoginManager()
login_manager.login_view = 'auth.sign_in'
oauth = OAuth()
admin = Admin()


def create_app(config_name="default"):
    flask_app = Flask(__name__)
    flask_app.config.from_object(config[config_name])
    config[config_name].init_app(flask_app)

    bootstrap.init_app(flask_app)
    mail.init_app(flask_app)
    db.init_app(flask_app)
    login_manager.init_app(flask_app)
    oauth.init_app(flask_app)
    admin.init_app(flask_app)

    from .main import main as main_blueprint
    flask_app.register_blueprint(main_blueprint)
    from .auth import auth as auth_blueprint
    flask_app.register_blueprint(auth_blueprint, url_prefix='/auth')

    return flask_app
