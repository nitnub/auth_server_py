from flask_jwt_extended import create_access_token, create_refresh_token


def create_fresh_tokens_obj(user_id: int) -> object:
    """Return a refresh token and "fresh" access token for the given id."""
    uid = str(user_id)
    access_token = create_access_token(identity=uid, fresh=True)
    refresh_token = create_refresh_token(identity=uid)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token
    }
