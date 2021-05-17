from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config
import stripe
import os
db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'authentication.login'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)




    from .blueprints.shop import bp as shop_bp
    app.register_blueprint(shop_bp)

    from .blueprints.authentication import bp as auth_bp
    app.register_blueprint(auth_bp)

    from .blueprints.api import bp as api_bp
    app.register_blueprint(api_bp)
    
    
    return app

