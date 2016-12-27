from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.pagedown import PageDown
from flask.ext.login import LoginManager
from flask.ext.bootstrap import Bootstrap
from flask.ext.misaka import Misaka
from config import Config

db = SQLAlchemy()
bootstrap = Bootstrap()
login_manager = LoginManager()
pagedown = PageDown()
md=Misaka()
login_manager.session_protection = 'basic'
login_manager.login_view = 'main.login'

def create_app():
	app = Flask(__name__)

	app.config.from_object(Config)
	Config.init_app(app)

	db.init_app(app)
	pagedown.init_app(app)
	login_manager.init_app(app)
	bootstrap.init_app(app)
	md.init_app(app)

	from .main import main as main_blueprint
	app.register_blueprint(main_blueprint)

	return app

