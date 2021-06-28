from flask import Flask
from config import Config
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_fontawesome import FontAwesome
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
fa = FontAwesome(app)
login_manager = LoginManager(app)

from app.routes import *

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)