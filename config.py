import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:

    SQLALCHEMY_DATABASE_URI ='sqlite:///' + os.path.join(basedir, 'data.sqlite')
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SECRET_KEY = 'i bet you don not know the key'

    @staticmethod
    def init_app(app):
    	pass
