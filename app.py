import os

from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_smorest import Api
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

from db import db
from cache import cache

from resources import UserBluePrint, MFABluePrint
from utils import Log


def create_app(db_url=None):
    app = Flask(__name__)
    load_dotenv()

    app.config["API_TITLE"] = "User authentication API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.2.0"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db")

    # register db
    db.init_app(app)
    Migrate(app, db)

    api = Api(app)

    # setup logging
    log_file = os.getenv("LOGFILE_NAME")
    if log_file:
        Log.register_log_file(log_file)

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

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({
            "message": "The token has expired.",
            "error": "token_expired",
            "success": False
        }), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({
            "message": "Unable to verify token signature.",
            "error": "token_invalid",
            "success": False
        }), 401

    # # create tables if not present... remove.. switched to migrate
    # with app.app_context():
    #     db.create_all()

    @app.before_request
    def start_request():
        Log.incoming(request)

    @app.after_request
    def end_request(response):
        Log.result(request, response)
        return response

    api.register_blueprint(UserBluePrint)
    api.register_blueprint(MFABluePrint)

    return app
