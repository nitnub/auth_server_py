import os
import redis
from datetime import datetime, timezone

 
class TokenCache():
    def __init__(self):
        self.r = redis.Redis(
            host = os.getenv("REDIS_HOST"),
            port = os.getenv("REDIS_PORT"),
            db = os.getenv("REDIS_DB"),
            username = os.getenv("REDIS_USERNAME"),
            password = os.getenv("REDIS_PASSWORD"),
            
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


    # check if token is blacklisted 
    def is_blacklisted(self, jti):
        try:
            if not jti:
                print("Error checking blocklist for jti, malformed request.")
                return True
            return self.r.get(jti) is not None
        except Exception as e:
            print("Error checking blocklist for jti", e)
            return False


cache = TokenCache()