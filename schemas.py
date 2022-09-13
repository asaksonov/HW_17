from marshmallow import Schema, fields


class DirectorSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String()


class GenreSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String()

class MovieSchema(Schema):
    id = fields.Integer(dump_only=True)
    title = fields.String()
    description = fields.String()
    trailer = fields.String()
    year = fields.Integer()
    rating = fields.Float()

    genre = fields.Nested(GenreSchema)

    director = fields.Nested(DirectorSchema)

