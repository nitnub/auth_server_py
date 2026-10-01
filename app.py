import os

from dotenv import load_dotenv
from flask import Flask
from flask_smorest import Api
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

from db import db
from cache import cache
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
    migrate = Migrate(app, db)

    api = Api(app)


    # JWTs
    # TODO: isolate config?
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
    jwt = JWTManager(app)

    # JWT Blocklist
    @jwt.token_in_blocklist_loader
    def token_in_blocklist(jwt_header, jwt_payload):
        jti = jwt_payload.get("jti")
        if not jti:
            print("Error checking blacklist: jti not provided.")
            return True
        return cache.is_blacklisted(jti)


    # # create tables if not present... remove.. switched to migrate
    # with app.app_context():
    #     db.create_all()


    api.register_blueprint(UserBluePrint)

    return app

