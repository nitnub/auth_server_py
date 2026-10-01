from datetime import datetime, timezone
import time

from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt, get_jti, get_jwt_identity, jwt_required
from sqlalchemy.exc import IntegrityError

from passlib.hash import pbkdf2_sha256
from db import db
from cache import cache

from models import UserModel, TokenModel
from schemas import UserSchema, SignInSchema


bp = Blueprint("Users", __name__, description="User operations")

@bp.route("/register")
class RegisterUser(MethodView):
    @bp.arguments(UserSchema)
    def post(self, user_data):

        print(user_data)
        try:
            user_hashed = {
                **user_data, 
                "password": pbkdf2_sha256.hash(user_data["password"])
                }

            user = UserModel(**user_hashed)

            db.session.add(user)
            db.session.commit()
            return {"message": "User created successfully."}, 201
        except TypeError as e:
            abort(400, "Invalid argument(s).")
        except IntegrityError:
            abort(409, "Username already in use.")




@bp.route("/signin")
class SignIn(MethodView): 
    @bp.arguments(SignInSchema)
    def post(self, user_data):
        try:        
            user = UserModel.query.filter(UserModel.email == user_data["email"]).first()

            if user and pbkdf2_sha256.verify(user_data["password"], user.password):
                access_token = create_access_token(identity=str(user.id), fresh=True)
                refresh_token = create_refresh_token(identity=str(user.id))
                return {"access_token": access_token, "refresh_token": refresh_token}

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
        # jti = jwt.get("jti")
        # exp = jwt.get("exp")
        # cache.blacklist(jti, exp)
        cache.blacklist(jwt.get("jti"), jwt.get("exp"))
        return {"success": True, "message": "Signed out successfully."}



@bp.route("/token")
class TokenRefresh(MethodView):
    @jwt_required(refresh=True)
    def post(self):

        # current_user = get_jwt_identity()  
        # new_token = create_access_token(identity=current_user, fresh=False)
        token = create_access_token(identity=get_jwt_identity(), fresh=False)
        return {"access_token": token}

        # return {
        #     "access_token": 
        #         create_access_token(
        #             identity=get_jwt_identity(), 
        #             fresh=False
        #         )
        #     }









    # @app.post('/signout')
    # def sign_out():
    #     pass

    # @app.post('/signin-oauth')
    # def sign_in_oauth():
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


@bp.route("/test")
class TestRequest(MethodView):
    @jwt_required()
    def post(self):

        # current_utc = int(datetime.now(timezone.utc).timestamp())
        # current_utc_now = int(datetime.utcnow().timestamp())
        # # current_utc = datetime.now(timezone.utc).total_seconds()
        # current_utc = int(time.time())



        # # date = datetime.utcfromtimestamp(current_utc / 1e3)
        # # date = datetime.utcfromtimestamp(current_utc)
        # date = datetime.now(timezone.utc)
        # print("current time       :", current_utc)
        # print("current time UTCNow:", current_utc_now)
        # print("time.time          :", current_utc)
        # print("jwt iat time       :", get_jwt().get("iat"))

        # print(date)
        # print(date)


        # print("jti:", get_jwt().get("jti"))
        # print("get_jwt_identity:", get_jwt_identity())
        # print("get_jti:", get_jti())
        # print("exp:", get_jwt().get("exp"))
        
        cur_time = int(datetime.now(timezone.utc).timestamp())
        # iat_time = get_jwt().get("iat")
        exp_time = get_jwt().get("exp")
        # exp_time = datetime.utcfromtimestamp(get_jwt().get("exp"))
        print("current time   :", cur_time)
        print("exp time       :", exp_time)
        # print("iat time       :", iat_time)
        print("duration       :", exp_time - cur_time)
        ct_test = datetime.now(timezone.utc)
        print("ct_test        :", ct_test)

        # cur_time = datetime.now(timezone.utc)
        cur_time = datetime.utcnow()
        iat_time = datetime.utcfromtimestamp(get_jwt().get("iat"))
        exp_time = datetime.utcfromtimestamp(get_jwt().get("exp"))

        print("moo")
        return {
            "jti_________": get_jwt().get("jti"),
            "iat__as__int": get_jwt().get("iat"),
            "current_time": cur_time, 
            "iat_____time": iat_time,
            "exp_____time": exp_time,
            "is___expired": cur_time > exp_time
            }, 200


        # TokenModel.query.filter(TokenModel.exp < current_time):

        token = TokenModel(
            jti = "test_jti_value",
            iat = cur_time,
            exp = cur_time,
            iaDateTime = cur_time,
            iaTime = cur_time,
        )


        db.session.add(token)
        db.session.commit()