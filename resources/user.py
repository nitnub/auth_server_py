from flask.views import MethodView
from flask_smorest import Blueprint, abort

from db import db


from models.user import UserModel
from schemas.user import UserSchema


bp = Blueprint("Users", __name__, description="Users operations")

@bp.route("/register")
class RegisterUser(MethodView):
    @bp.arguments(UserSchema)
    def post(self, user_data):
        return user_data






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
