import os


class BaseConfig(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.getenv('SECRET_KEY')
    ENDPOINTS = {
        'blogs': os.getenv('BLOGS_ENDPOINT'),
        'comments': os.getenv('COMMENTS_ENDPOINT'),
        'posts': os.getenv('POSTS_ENDPOINT'),
        'users': os.getenv('USERS_ENDPOINT'),
    }


class DevConfig(BaseConfig):
    DEBUG = True


class TestConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    PRESERVE_CONTEXT_ON_EXCEPTION = False


class ProdConfig(BaseConfig):
    pass


environments = {
    'prod': ProdConfig,
    'dev': DevConfig,
    'test': TestConfig
}
