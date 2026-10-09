import os
import redis
from datetime import datetime, timezone

REDIS_DEFAULT_PORT = 6379


class TokenCache():
    def __init__(self):
        self.r = redis.Redis(
            host=os.getenv("REDIS_HOST"),
            port=os.getenv("REDIS_PORT", REDIS_DEFAULT_PORT),
            db=os.getenv("REDIS_DB")
        )

    # blacklist a token
    def blacklist(self, jti, exp_time):
        try:
            # get current time
            cur_time = int(datetime.now(timezone.utc).timestamp())

            # calculate and set ttl
            ttl = exp_time - cur_time
            self.r.setex(jti, ttl, 1)

            return True
        except Exception as e:
            print("Error adding jti to blacklist", e)
            return False

    # # check if token is blacklisted
    # def is_blacklisted(self, jti):

    #     if not jti:
    #         print("Error checking blocklist for jti, malformed request.")
    #         return True

    #     return self.r.get(jti) is not None

    # check if token is blacklisted
    def is_blacklisted(self, jti):
        try:
            return self.r.get(jti) is not None
        except Exception as e:
            print("Cache error:", e)  # TODO: Add to logger.. default to block
            return True


    # save data for 2fa
    def save_confirmation(self, request_id, confirmation_code):
        if not request_id or confirmation_code:
            return False
        ttl = 60 * 5  # 5 mins... 
        self.r.setex(request_id, ttl, confirmation_code)
        return True

    def is_valid_confirmation(self, request_id, confirmation_code):
        prior_code = self.r.get(request_id)
        return prior_code and prior_code == confirmation_code


cache = TokenCache()
