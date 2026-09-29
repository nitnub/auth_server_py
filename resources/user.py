from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity
from sqlalchemy.exc import IntegrityError

from passlib.hash import pbkdf2_sha256
from db import db


from models.user import UserModel
from schemas.user import UserSchema, SignInSchema


bp = Blueprint("Users", __name__, description="User operations")

@bp.route("/register")
class RegisterUser(MethodView):
    @bp.arguments(UserSchema)
    def post(self, user_data):

        print(user_data)
        try:
            # user = {**user_data, "password": "moo"}
            user_hashed = {**user_data, "password": pbkdf2_sha256.hash(user_data["password"])}
            # print()
            # validate fields
            # user = UserModel(**{**user_data, "password": "__hashed!", "test1": "some data", "cabbage": 123})
            # user = UserModel(**{**user_data, "password": "__hashed!"})
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
                print(user)
                print(user.id)
                access_token = create_access_token(identity=str(user.id), fresh=True)
                refresh_token = create_refresh_token(identity=str(user.id))

                return {"access_token": access_token, "refresh_token": refresh_token}
                return {"success": True}

            return {"success": False}
        except Exception  as e:
            print(e)
            abort(500, "Unknown error.")

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
