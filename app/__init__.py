from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy

from config import Config

app = Flask(__name__)
app.config.from_object(Config)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost:3306/flasknote'
# app.config['SECRET_KEY'] = 'qwertyuiop'

db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'

bootstrap = Bootstrap(app)
# login = LoginManager(app)
# login.login_view = 'login'

# @login.user_loader
# def load_user(user_id):
#     user = db.session.query(User).get(user_id)
#     return user


manager = Manager(app=app)
manager.add_command('db', MigrateCommand)

# def create_app():
#     app = Flask(__name__)
#     app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost:3306/note1'
#     app.config['SECRET_KEY'] = 'qwertyuiop'
#     db.init_app(app)
#     Bootstrap(app)
#
#     return app


from app import routes, models, forms

