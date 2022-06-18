from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager
from flask_select2 import Select2
from flask_migrate import Migrate
from flask_principal import Principal

app = Flask(__name__, static_folder='static')
app.config.from_object('config')

db = SQLAlchemy(app)
csrf = CSRFProtect(app)
migrate = Migrate(app, db)

# Flask-principal
principals = Principal(app)

# Flask Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

from routes import *

# select2
select2 = Select2()
select2.init_app(app)
select2.add_loader(loader=tag_loader)

"""
- Settings --> Header index post, description blog, featured post
- assets.py
"""