
from flask.views import MethodView
from flask_smorest import Blueprint, abort


from cache import cache

from models import UserModel
from schemas import EmailRequestSchema, EmailConfirmSchema

bp = Blueprint("Email Requests", __name__, description="MFA email requests")


@bp.route("/mfa/email")
class EmailRequest(MethodView):
    @bp.arguments(EmailRequestSchema)
    def post(self, user_data):

        # receive user email

        # verify email / user
        user = UserModel.query.filter(UserModel.email == user_data["email"]).first()
        # user gives username
        if not user:
            # do not want to hint to bad actors that user doesn't exist...
            # artificial time delay?
            return {"success": True, "message": "Request processed."}

        # secret code is generated
        confirmation_code = "abc123"
        request_id = "a-unique-alpha-numeric-id"
        # confirmation_code is placed in redis cache with request_id as key? TTL of 10 mins?
        cache.save_confirmation(request_id, confirmation_code)

        # email is sent to associated user email with secret code
        # email.send(user_email, code)
        # if an error sending that acknowledged email is real, alert user.. if not, send generic success message
        # response is sent to requestor with request id / secret id for this request


@bp.route("/mfa/emailconfirm")
class EmailConfirm(MethodView):
    @bp.arguments(EmailConfirmSchema)
    def post(self, user_email):

        # receive user secret id and secret code

        # verify email / user

        # user gives username

        # secret code is generated
        # secret code is placed in redis cache with userID as key? TTL of 10 mins?

        # email is sent to associated user email with secret code

        # USE A SECRET ID IN PLACE OF THE USERNAME FOR THE SECOND REQUEST?
        #   IS THERE A GOOD WAY TO CONVEY THIS?

        # 2fa endpoint awaits entry of code

        # if code entered via 2fa endpoint, return access and refresh token.


        # response contains success message and temp ID associated with email...
