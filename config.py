import os
import secrets

secret =secrets.token_urlsafe(32)

class Config:
  SECRET_KEY = secret
  MAIL_SERVER = 'smtp.googlemail.com'
  MAIL_PORT = 587
  MAIL_USE_TLS = True
  MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
  MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
  UPLOADED_PHOTOS_DEST = 'app/static/photos'

# db test


class ProdConfig(Config):
    '''
    Production  configuration child class

    Args:
        Config: The parent configuration class with General configuration settings
    '''
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL","")
    
    if SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
        SQLALCHEMY_DATABASE_URI =SQLALCHEMY_DATABASE_URI.replace("postgres://","postgresql://",1)


class DevConfig(Config):
  # this is the location of the database with authentication.

  SQLALCHEMY_DATABASE_URI ='postgresql+psycopg2://axs:code@localhost/iconnect'
  
  DEBUG = True
#These dictionary help us access different configuration option classes.
config_options = {
  'development':DevConfig,
  'production':ProdConfig,
}