import os
import requests
import google.generativeai as genai
from flask import Flask, request, jsonify
from dotenv import load_dotenv

# importa os módulos criados
from context_handler import ContextHandler
from phishing_checker import analisar_texto

# Carrega as variáveis do arquivo .env
load_dotenv()

app = Flask(__name__)

# Configura a API do gemini
API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    raise ValueError("A chave de API não foi encontrada")
genai.configure(api_key=API_KEY)

# Inicializa o modelo
model = genai.GenerativeModel('models/gemini-1.5-flash')

# Inicia o gerenciador de contexto
context_handler = ContextHandler()

# DIcionário para armazenar o objeto do chat para cada usuário
chat_sessions = {}

# Endpoit para interagir com o sistema da assistente de IA
@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_id = data.get('user_id')
    user_message = data.get('message')

    if not user_id or not user_message:
        return jsonify({"error": "user_id e message são obrigatórios"}), 400

    response_message = ""
    analise_resultado = {"suspicious": False, "reason": "Nenhum indicador de phishing encontrado"}
    
    # 1. Determina se a mensagem é uma URL, e-mail ou texto comum
    user_message_lower = user_message.lower()
    
    if "http" in user_message_lower or "www." in user_message_lower:
        analise_resultado = analisar_texto(user_message, tipo="url")
    elif "@" in user_message_lower:
        analise_resultado = analisar_texto(user_message, tipo="email")
    # Se não for uma URL ou e-mail, a analise_resultado permanece não-suspeita
    
    # 2. Se a análise for suspeita, retorna o aviso
    if analise_resultado["suspicious"]:
        response_message = f"Cuidado! Esta mensagem pode ser um indício de phishing. Motivo: {analise_resultado['reason']}"
    else:
        # 3. Se a mensagem não for suspeita, interage com o modelo Gemini
        try:
            if user_id not in chat_sessions:
                chat_sessions[user_id] = model.start_chat(history=context_handler.get_history(user_id))
            
            chat_session = chat_sessions[user_id]
            
            context_handler.add_message(user_id, 'user', user_message)

            gemini_response = chat_session.send_message(user_message)
            response_message = gemini_response.text

            context_handler.add_message(user_id, 'model', response_message)

        except Exception as e:
            response_message = f"Ocorreu um erro ao processar a requisição: {e}"
    
    return jsonify({"response": response_message})

# Endpoit para reiniciar o contexto da conversa
@app.route('/reset', methods=['POST'])
def resetar_chat():
    data = request.json
    user_id = data.get('user_id')
    if user_id:
        context_handler.reset_session(user_id)
        if user_id in chat_sessions:
            del chat_sessions[user_id]
        return jsonify({"status": "ok", "message": "Sessão resetada"})
    return jsonify({"error": "user_id é obrigatório"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)