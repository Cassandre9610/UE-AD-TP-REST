from marshmallow import Schema, fields, validate


class UserCreateSchema(Schema):
    id = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=100)
    )
    name = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=100)
    )

    class Meta:
        unknown = "raise"