import os

from flask import Flask
from flask_smorest import Api
from dotenv import load_dotenv

from db import db
from models.user import UserModel
from resources.user import bp as UserBluePrint


def create_app():
    app = Flask(__name__)
    load_dotenv()



    app.config["API_TITLE"] = "User authentication API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.2.0"
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///data.db")

    # register db
    db.init_app(app)


    api = Api(app)
    api.register_blueprint(UserBluePrint)

    return app
    # @app.post('/register')
    # def register_user():
    #     # 
    #     pass

    # @app.post('/signin')
    # def sign_in():
    #     pass

    # @app.post('/signin-oauth')
    # def sign_in_oauth():
    #     pass

    # @app.post('/signout')
    # def sign_out():
    #     pass

    # @app.get('/token')
    # def refresh_token():
    #     pass


    # # email testing
    # @app.get('/2fa-email')
    # def request_2fa_email():
    #     pass

    # @app.post('/2fa-email')
    # def confirm_2fa_email():
    #     pass

