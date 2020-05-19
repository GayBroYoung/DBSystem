from flask import Flask
import os
from flask_bootstrap import Bootstrap

bootstrap = Bootstrap()

def create_app():
    app = Flask(__name__)
    from .watchlist import main as main_blueprint
    hostname = "localhost"
    config_str = "mysql+pymysql://root:123456@"
    table_name = "tables"
    from watchlist.models import db
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev')
    app.config['SQLALCHEMY_DATABASE_URI'] = config_str + hostname + "/" + table_name
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['SQLALCHEMY_ECHO'] = True
    app.config['BOOTSTRAP_SERVE_LOCAL'] = True
    app.debug = True
    app.register_blueprint(main_blueprint)
    bootstrap.init_app(app)
    db.init_app(app)

    return app