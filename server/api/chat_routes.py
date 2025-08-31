import os
import google.generativeai as genai

from flask import jsonify
from flask.views import MethodView
from flask_smorest import Blueprint
from context_handler import ContextHandler
from phishing_checker import analisar_texto
from schemas import ChatRequestSchema, ChatResponseSchema

# Inicializa o BLueprint para as rotas do "chat"
blp = Blueprint("Chat", __name__, url_prefix="/chat", description="Endpoints para o assistente")

# Configura API do Gemini
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel('models/gemini-1.5-flash')
context_handler = ContextHandler()
chat_sessions = {}

# Endpoint principal para interagir com o assistente
@blp.route("/")
class ChatResource(MethodView):
    @blp.arguments(ChatRequestSchema)
    @blp.response(200, ChatResponseSchema)
    def post(self, chat_data):
        user_id = chat_data.get('user_id')
        user_message = chat_data.get('message')

        response_message = ""
        user_message_lower = user_message.lower()
        analise_resultado = {"suspicius": False, "reason": "Nenhum indicador de phishing encontrado"}

        if "http" in user_message_lower or "www." in user_message_lower:
            analise_resultado = analisar_texto(user_message, tipo="url")
        elif "@" in user_message_lower:
            analise_resultado = analisar_texto(user_message, tipo="email")

        if analise_resultado["suspicious"]:
            response_message = f"Cuidado! Esta mensagem pode ser indicio de phishing. Motivo: {analise_resultado['reason']}"
        else:
            try:
                if user_id not in chat_sessions:
                    chat_sessions[user_id] = model.start_chat(history=context_handler.get_history(user_id))

                chat_sessions = chat_sessions[user_id]

                context_handler.add_message(user_id, 'user', user_message)
                gemini_response = chat_sessions.send_message(user_message)
                response_message = gemini_response.text
                context_handler.add_message(user_id, 'model', response_message)

            except Exception as e:
                response_message = f"Ocorreu u merro ao porcessar a requisição: {e}"

        return jsonify({"response": response_message})