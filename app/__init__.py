from flask import Flask
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_mysqldb import MySQL
from .config import Config, config
from .auth import auth
from app.models import UserModel


login_manager = LoginManager()
login_manager.login_view = 'auth.login'


@login_manager.user_loader
def load_user(username):
    return UserModel.query(username)


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config.from_object(config['development'])
    login_manager.init_app(app)
    app.register_blueprint(auth)
    bootstrap = Bootstrap(app)

    return app


