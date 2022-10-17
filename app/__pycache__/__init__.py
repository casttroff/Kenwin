from flask import Flask
from flask_bootstrap import Bootstrap
from flask_mysqldb import MySQL
from .config import Config, config
from .auth import auth


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config.from_object(config['development'])
    app.register_blueprint(auth)
    bootstrap = Bootstrap(app)

    return app


