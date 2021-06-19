from flask import Flask
from config import config_options
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_login import LoginManager
from flask_uploads import UploadSet, configure_uploads, IMAGES

db = SQLAlchemy()
mail = Mail()
bootstrap = Bootstrap()
photos = UploadSet('photos', IMAGES)

login_manager = LoginManager()

def create_app(config_name):
  app = Flask(__name__)

  app.config.from_object(config_options[config_name])

  from .main import main as main_blueprint
  app.register_blueprint(main_blueprint)

  from .auth import auth as auth_blueprint
  app.register_blueprint(auth_blueprint, url_prefix= '/authenticate')

  # initalisin extensions
  bootstrap.init_app(app)

  return app
  