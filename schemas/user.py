from marshmallow import Schema, fields

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    email = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)  # load only!! we don't ever want to return password info to an API call

    firstName = fields.Str(required=False)
    lastName = fields.Str(required=False)
    avatar = fields.Str(required=False)
    admin = fields.Bool(required=False)
    active = fields.Bool(required=False)
    authProvider = fields.Int(required=False)


class SignInSchema(Schema):
    email = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)  # load only!! we don't ever want to return password info to an API call
