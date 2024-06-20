import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or "Venzeslav"
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or "smtp.googlemail.com"
    MAIL_PORT = os.environ.get('MAIL_PORT') or "587"
    MAIL_USE_TLS = int(os.environ.get('MAIL_USE_TLS', '5870'))
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or "lminlisa@gmail.com"
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or "pexc qtqh kfwd rnvs"
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
                              'mysql://root:@localhost/flaskkk'


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
                              'mysql://root:@localhost/flaskkk'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
                              'mysql://root:@localhost/flaskkk'


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
