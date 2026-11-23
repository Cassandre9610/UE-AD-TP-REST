from marshmallow import Schema, fields, validate


class MovieCreateSchema(Schema):
    title = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=100)
    )
    rating = fields.Int(
        required=True,
        validate=validate.Range(min=0, max=10)
    )
    director = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=100)
    )

    class Meta:
        unknown = "raise"