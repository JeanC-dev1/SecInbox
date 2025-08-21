# server/context_handler.py

class ContextHandler:
    #Gerencia o histórico de conversas para a sessão de chat.
    #Cada usuário terá seu próprio histórico armazenado em memória.
    def __init__(self):
        # Dicionário para armazenar o histórico de cada usuário.
        # A chave será o ID do usuário e o valor
        self.sessions = {}

    def add_message(self, user_id, role, content):
        #Adiciona uma nova mensagem ao histórico de um usuário
        if user_id not in self.sessions:
            self.sessions[user_id] = []
        
        self.sessions[user_id].append({'role': role, 'parts': [content]})

    def get_history(self, user_id):
        #Retorna o histórico de conversas de um usuário.
        return self.sessions.get(user_id, [])

    def reset_session(self, user_id):
        #Limpa o histórico de conversas de um usuário.
        if user_id in self.sessions:
            self.sessions[user_id] = []