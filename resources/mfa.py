import uuid
import random
import string

from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import create_access_token, create_refresh_token

from cache import cache
from models import UserModel
from schemas import EmailRequestSchema, EmailConfirmSchema

from mfa import send_mfa_email
from utils import create_fresh_tokens_obj

bp = Blueprint("Email Requests", __name__, description="MFA email requests")


def _generate_confirmation_code(length: int = 8) -> str:
    """Generate a raw MFA confirmation code."""
    arr = random.choices(
            string.ascii_letters + string.digits,
            k=length
        )
    # arr[length//2] = '-'
    return "".join(arr)


def _format_confirmation_code(raw_code: str) -> str:
    """Add formatting to a raw MFA confirmation code for added readability."""
    mid = len(raw_code) // 2
    return f"{raw_code[:mid]}-{raw_code[mid:]}"


def _get_user_by_email(user_email: str):
    """Find user by email. Returns None if user not found."""
    return UserModel.query.filter(UserModel.email == user_email).first()


@bp.route("/mfa/email")
class EmailRequest(MethodView):
    @bp.arguments(EmailRequestSchema)
    def post(self, user_data):  # TODO: consolidate returns or reorder...
        # TODO: artifical time delay to obscure success/failure?
        try:
            # create request id
            request_id = str(uuid.uuid4())
            user = _get_user_by_email(user_data["email"])

            # check for valid user
            if user:
                # store confirmation code in redis cache
                code = _generate_confirmation_code()
                cache.save_confirmation(request_id, code)

                # send email to user with secret code
                formatted_code = _format_confirmation_code(code)
                send_mfa_email(user.email, formatted_code)
            else:
                # TODO:  keep logs of this? add to a logger
                print("Invalid user request for", user_data["email"])
        except Exception as e:
            print("error sending email request:", e)
            # if an internal error, ok to surface to user...
            # TODO: change to abort()
            return {
                "success": False,
                "message": "Internal error while processing request."
            }, 500
        finally:
            # send success if real or fake email was received
            return {
                "success": True,
                "message": "Request processed.",
                "request_id": request_id
            }

@bp.route("/mfa/emailconfirm")
class EmailConfirm(MethodView):
    @bp.arguments(EmailConfirmSchema)
    def post(self, user_data):

        # verify email / user
        user = _get_user_by_email(user_data["email"])
        if not user:
            # TODO: add aborts...
            print("Not a valid user..")
            return {
                "success": False,
                "message": "Error processing request."
            }

        # if match, return access and refresh token.
        if cache.is_valid_confirmation(user_data["temp_id"], user_data["code"]):
            # prevent multiple requests from one temp_id
            cache.remove_confirmation(user_data["temp_id"])
            tokens = create_fresh_tokens_obj(user.id)
            return {"success": True, **tokens}, 200
        print("Not a valid confirmation..")
        return {
            "success": False,
            "message": "Invalid confirmation code."
        }
