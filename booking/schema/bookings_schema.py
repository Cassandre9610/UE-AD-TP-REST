from marshmallow import Schema, fields, validate


class BookingCreateSchema(Schema):
    userid = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=100)
    )
    date = fields.Str(
        required=True,
        validate=validate.Regexp(r"^\d{8}$")
    )
    movieid = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=100)
    )

    class Meta:
        unknown = "raise"
