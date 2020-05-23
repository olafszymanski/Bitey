import os


class Config:
    DEBUG = False
    SECRET_KEY = os.getenv('BITEY_SECRET_KEY')
    SECURITY_PASSWORD_SALT = os.getenv('BITEY_SECURITY_PASSWORD_SALT')
    SQLALCHEMY_DATABASE_URI = os.getenv('BITEY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_PROTECTION = 'strong'
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_DEFAULT_SENDER  = 'bitey.app@gmail.com'
    MAIL_USERNAME = os.getenv('BITEY_MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('BITEY_MAIL_PASSWORD')


class DebugConfig(Config):
    DEBUG = True
