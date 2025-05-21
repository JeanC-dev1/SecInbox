import re
import os
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env (se existir)
def carregar_env():
    load_dotenv()

# Valida e-mail simples usando regex
def validar_email(email):
    padrao = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(padrao, email) is not None

# Valida URL simples
def validar_url(url):
    padrao = r'^(http|https)://[^\s]+$'
    return re.match(padrao, url) is not None

# Limpa texto removendo espaços extras e caracteres invisíveis
def limpar_texto(texto):
    return ' '.join(texto.strip().split())

# Exemplo para carregar variável do .env
def obter_chave_virustotal():
    carregar_env()
    return os.getenv('VT_API_KEY', '')

# Função para formatar texto para exibir (pode ser usada para logs ou UI)
def formatar_resultado(suspeito, motivo):
    status = "Suspeito" if suspeito else "Seguro"
    return f"[{status}] - {motivo}"

