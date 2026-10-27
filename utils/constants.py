from enum import StrEnum, IntEnum


class Constants:
    class Env(StrEnum):
        # Logging
        LOGFILE_NAME = "LOGFILE_NAME"

        # If running normally:
        DATABASE_URL = "DATABASE_URL"
        JWT_SECRET_KEY = "JWT_SECRET_KEY"

        # Redis
        REDIS_HOST = "REDIS_HOST"
        REDIS_PORT = "REDIS_PORT"
        REDIS_DB = "REDIS_DB"
        REDIS_USERNAME = "REDIS_USERNAME"
        REDIS_PASSWORD = "REDIS_PASSWORD"

        # MFA
        MFA_EMAIL_ADDRESS = "MFA_EMAIL_ADDRESS"
        MFA_EMAIL_PASSWORD = "MFA_EMAIL_PASSWORD"
        MFA_EMAIL_TEST_RECIPIENT = "MFA_EMAIL_TEST_RECIPIENT"
        MFA_EMAIL_SMTP = "MFA_EMAIL_SMTP"

        # Testing
        TEST_DATABASE_URL = "TEST_DATABASE_URL"

    class StatusCode(IntEnum):
        OK = 200
        CREATED = 201
        BAD_REQUEST = 400
        UNAUTHORIZED = 401
        CONFLICT = 409
        INTERNAL_ERROR = 500

    class Strings(StrEnum):
        SQLITE_URL = "sqlite:///data.db"


Const = Constants()
