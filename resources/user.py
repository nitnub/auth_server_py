from datetime import datetime, timezone
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt, get_jti, get_jwt_identity, jwt_required
from sqlalchemy.exc import IntegrityError

from passlib.hash import pbkdf2_sha256 as h
from db import db
from cache import cache

from models import UserModel
from schemas import UserSchema, SignInSchema

from mfa import send_mfa_email

bp = Blueprint("Users", __name__, description="User operations")


@bp.route("/register")
class RegisterUser(MethodView):
    @bp.arguments(UserSchema)
    def post(self, user_data):

        print(user_data)
        try:
            user_hashed = {
                **user_data,
                "password": h.hash(user_data["password"])
                }

            user = UserModel(**user_hashed)

            db.session.add(user)
            db.session.commit()
            return {"message": "User created successfully."}, 201
        except TypeError:
            abort(400, "Invalid argument(s).")
        except IntegrityError:
            abort(409, "Username already in use.")


@bp.route("/signin")
class SignIn(MethodView):
    @bp.arguments(SignInSchema)
    def post(self, user_data):
        try:
            user = UserModel.query.filter(UserModel.email == user_data["email"]).first()

            if user and h.verify(user_data["password"], user.password):
                uid = str(user.id)
                access_token = create_access_token(identity=uid, fresh=True)
                refresh_token = create_refresh_token(identity=uid)

                return {
                    "access_token": access_token,
                    "refresh_token": refresh_token
                }

            abort(401, message="Invalid credentials.")
        except Exception as e:
            print(e)
            abort(500, "Unknown error.")


@bp.route("/signout")
class SignOut(MethodView):
    @jwt_required()
    def post(self):
        # blacklist jti
        jwt = get_jwt()
        cache.blacklist(jwt.get("jti"), jwt.get("exp"))
        return {"success": True, "message": "Signed out successfully."}


@bp.route("/token")
class TokenRefresh(MethodView):
    @jwt_required(refresh=True)
    def post(self):
        token = create_access_token(identity=get_jwt_identity(), fresh=False)
        return {"access_token": token}

    # TODO: o-auth...
    # @app.post('/signin-oauth')
    # def sign_in_oauth():
    #     pass

    # @app.post('/signout-oauth')
    # def sign_out_oauth():
    #     pass

@bp.route("/test")
class TestRequest(MethodView):
    @jwt_required()
    def post(self):

        tst = send_mfa_email("email address", 987654321)
        return {"success": True, "temp_identifier": 987654321}
