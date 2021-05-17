import os
from dotenv import load_dotenv
import stripe


basedir = os.path.abspath(os.path.dirname(__name__))
#load_dotenv(os.path.join(basedir, '.env'))

class Config:
    FLASK_APP = os.getenv('FLASK_APP')
    FLASK_ENV = os.getenv('FLASK_ENV')
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS')
    SECRET_KEY = os.getenv('SECRET_KEY')
    STRIPE_SECRET_KEY=os.getenv('STRIPE_SECRET_KEY')
    STRIPE_PUBLISHABLE_KEY=os.getenv('STRIPE_PUBLISHABLE_KEY')
    stripe.api_key = STRIPE_SECRET_KEY