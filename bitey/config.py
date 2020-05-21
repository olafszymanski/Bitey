class Config:
    DEBUG = False
    SECRET_KEY = '5f404452bae4eb7db44800a3d787cdb1'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///bitey.sqlite3'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DebugConfig(Config):
    DEBUG = True
