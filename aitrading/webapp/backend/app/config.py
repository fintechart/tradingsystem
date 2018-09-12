# coding=utf-8

import os

basedir = os.path.abspath(os.path.dirname(__file__))
maria_local_base = 'mysql+pymysql://root:myr00t@localhost:3306/tradingsystem'

class BaseConfig:
    """Base configuration."""
    SECRET_KEY = os.getenv('SECRET_KEY', 'supersecret')
    DEBUG = False
    BCRYPT_LOG_ROUNDS = 7 
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(BaseConfig):
    """Development configuration."""
    SECRET_KEY = 'nooneknows'
    DEBUG = True
    BCRYPT_LOG_ROUNDS = 4
    SQLALCHEMY_DATABASE_URI = maria_local_base


class TestingConfig(BaseConfig):
    """Testing configuration."""
    DEBUG = True
    TESTING = True
    BCRYPT_LOG_ROUNDS = 4
    SQLALCHEMY_DATABASE_URI = maria_local_base + '_test'
    PRESERVE_CONTEXT_ON_EXCEPTION = False


class ProductionConfig(BaseConfig):
    """Production configuration."""
    SECRET_KEY = 'supersecret'
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'mariadb:///proddb'
