import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    CLIENT_ID = os.environ.get('CLIENT_ID') or ''
    CLIENT_SECRET = os.environ.get('CLIENT_SECRET') or ''
    API_KEY = os.environ.get('API_KEY') or ''
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False