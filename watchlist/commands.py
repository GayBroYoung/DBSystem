from flask import Flask
import os
import sys
sys.path.append('E:/DeskTopFiles/19-20/数据库/flask_proj/')
from flask_sqlalchemy import SQLAlchemy

from flask_script import Manager,Command,Shell
from sqlalchemy import func
from flask_migrate import Migrate,MigrateCommand

from watchlist.models import db
# from app import app
from watchlist import models as data
from watchlist.models import db
app = Flask(__name__)

config_str = "mysql+pymysql://root:123456@localhost/"
table_name = "tables"

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev')
app.config['SQLALCHEMY_DATABASE_URI'] = config_str + table_name
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_ECHO'] = True

db.init_app(app)
manager = Manager(app)
migrate = Migrate(app,db)

manager.add_command('db',MigrateCommand)


def make_shell_context():
    return dict(app=app,db=db,models=data)


manager.add_command("Shell",Shell(make_context=make_shell_context))





if __name__ == '__main__':
    manager.run()