from marshmallow import Schema, fields


class UrlSchema(Schema):
    url = fields.URL(required=True)
