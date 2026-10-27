import os
import redis
from datetime import datetime, timezone
from utils import Constants

Env = Constants.Env
REDIS_DEFAULT_PORT = 6379


class TokenCache():  # TODO: update name? more general?
    def __init__(self):
        self.r = redis.Redis(
            host=os.getenv(Env.REDIS_HOST),
            port=os.getenv(Env.REDIS_PORT, REDIS_DEFAULT_PORT),
            db=os.getenv(Env.REDIS_DB)
        )

    # blacklist a token
    def blacklist(self, jti, exp_time):
        try:
            # get current time
            cur_time = int(datetime.now(timezone.utc).timestamp())

            # calculate and set ttl
            ttl = exp_time - cur_time + 1  # add 1 sec to force overlap
            self.r.setex(jti, ttl, 1)

            return True
        except Exception as e:
            print("Error adding jti to blacklist", e)
            return False

    # check if token is blacklisted
    def is_blacklisted(self, jti):
        try:
            return self.r.get(jti) is not None
        except Exception as e:
            print("Cache error:", e)  # TODO: Add to logger.. default to block
            return True

    # save data for 2fa
    def save_confirmation(self, request_id: str, confirmation_code: str):
        if not request_id or not confirmation_code:
            return False
        ttl = 60 * 5  # 5 mins...
        self.r.set(request_id, confirmation_code, ex=ttl)
        return True

    def is_valid_confirmation(self, request_id: str, confirmation_code: str):
        """Verify the given request id -> confirmation code pair is valid."""
        prior_code = self.r.get(request_id)
        formatted_confirmation = confirmation_code.replace('-', '')
        return prior_code and prior_code.decode() == formatted_confirmation

    def remove_confirmation(self, request_id: str):
        """Remove the given request id from the cache to avoid reuse."""
        return self.r.delete(request_id) != 0


cache = TokenCache()
