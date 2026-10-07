from marshmallow import Schema, fields


class EmailRequestSchema(Schema):
    email = fields.Str(required=True)


class EmailConfirmSchema(Schema):
    temp_id = fields.Str(required=True)
    code = fields.Str(required=True)

