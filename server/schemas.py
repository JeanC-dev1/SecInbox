from marshmallow import Schema, fields
from marshmallow.validate import OneOf

class ChatResponseSchema(Schema):
    response = fields.String(required=True)

class CheckerSchema(Schema):
    texto = fields.String(required=True)
    tipo = fields.String(required=True, validate=OneOf(["url", "email"]))
