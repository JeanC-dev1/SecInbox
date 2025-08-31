from marshmallow import Schema, fields

class ChatRequestSchema(Schema):
    user_id = fields.String(required=True)
    message = fields.String(required=True)

class ChatResponseSchema(Schema):
    response = fields.String(required=True)