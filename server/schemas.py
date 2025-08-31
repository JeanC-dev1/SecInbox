from marshmallow import Schema, fields

class ChatRequestSchema(Schema):
    user_id = fields.String(required=True, description="ID único do usuário.")
    message = fields.String(required=True, description="Mensagem ou texto para ser analisado.")

class ChatResponseSchema(Schema):
    response = fields.String(required=True, description="A resposta da assistente de IA ou aviso de phishing")