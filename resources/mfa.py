import uuid
import random
import string

from flask.views import MethodView
from flask_smorest import Blueprint

from cache import cache

from models import UserModel
from schemas import EmailRequestSchema, EmailConfirmSchema

from mfa import send_mfa_email

bp = Blueprint("Email Requests", __name__, description="MFA email requests")


def generate_confirmation_code(length: int = 8) -> str:
    arr = random.choices(
            string.ascii_letters + string.digits,
            k=length + 1
        )
    arr[length//2] = '-'
    return "".join(arr)


@bp.route("/mfa/email")
class EmailRequest(MethodView):
    @bp.arguments(EmailRequestSchema)
    def post(self, user_data):  # TODO: consolidate returns or reorder...
        # TODO: artifical time delay to obscure success/failure?
        try:
            # create request id
            request_id = uuid.uuid4()

            # verify email / user
            user = UserModel.query.filter(UserModel.email == user_data["email"]).first()

            # check for valid user
            if not user:
                # do not want to hint to bad actors that user doesn't exist...
                # artificial time delay?
                return {
                    "success": True,
                    "message": "Request processed.",
                    "request_id": request_id
                }

            # generate confirmation code
            confirmation_code = generate_confirmation_code()

            # confirmation code is placed in redis cache with request_id as key
            cache.save_confirmation(request_id, confirmation_code)

            # email is sent to associated user email with secret code
            send_mfa_email(user["email"], confirmation_code)

            return {
                "success": True,
                "message": "Request processed.",
                "request_id": request_id
            }
        except Exception as e:
            print("error sending email request:", e)
            # if an error sending that acknowledged email is real, alert user..
            #   if not, send generic success message
        finally:
            # send success if real or fake email, but transparent about errors?
            return {
                "success": False,
                "message": "Error processing request."
                # "request_id": request_id
            }

@bp.route("/mfa/emailconfirm")
class EmailConfirm(MethodView):
    @bp.arguments(EmailConfirmSchema)
    def post(self, user_data):

        return {"message": "not implemented..."}
        # receive user secret id and secret code (and email?)

        # verify email / user

        # user gives username/email? (Send prefererd?)

        # if no match, send fail message.. user may have mistyped..
        # if match, return access and refresh token. ("not fresh")

        # should not distinguish between "secret id not found" and "id found but code doesn't match"
