import os
import google.generativeai as genai
from flask import Flask, jsonify, request
from flask_smorest import Api
from dotenv import load_dotenv

# Importa o Blueprint do seu novo arquivo de rotas
from api.chat_routes import blp as ChatBlueprint

# Importa os outros módulos (se necessário)
from context_handler import ContextHandler

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

app = Flask(__name__)

# Configurações do Flask-Smorest para a documentação
app.config["API_TITLE"] = "API SecureInbox"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.2"
app.config["OPENAPI_URL_PREFIX"] = "/"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

api = Api(app)
context_handler = ContextHandler() # Mantém a instância aqui se for usada em outras rotas

# Endpoint para reiniciar o contexto
@app.route('/reset', methods=['POST'])
def reset_chat():
    data = request.json
    user_id = data.get('user_id')
    if user_id:
        context_handler.reset_session(user_id)
        # O chat_sessions deve ser resetado no novo arquivo de rotas, ou no context_handler
        return jsonify({"message": "Sessão resetada"})
    return jsonify({"error": "user_id é obrigatório"}), 400

# Registra o Blueprint na API
api.register_blueprint(ChatBlueprint)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)