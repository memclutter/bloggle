import os


class BaseConfig(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.getenv('SECRET_KEY')


class DevConfig(BaseConfig):
    DEBUG = True


class TestConfig(BaseConfig):
    DEBUG = True
    TESTING = True


class ProdConfig(BaseConfig):
    pass


environments = {
    'prod': ProdConfig,
    'deve': DevConfig,
    'test': TestConfig
}
