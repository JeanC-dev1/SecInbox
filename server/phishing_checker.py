import os
import re
import requests
import whois
from urllib.parse import urlparse
from datetime import datetime

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

# CArrega uma lista de palavras de um arquivo de texto
def carregar_lista(nome_arquivo):
    caminho = os.path.join(DATA_DIR, nome_arquivo)
    try:
        with open(caminho, "r", encoding="utf-8") as f:
            return [linha.strip().lower() for linha in f if linha.strip()]
    except FileNotFoundError:
        return []
    
# Função principal para analisar texto como URL ou e-mail
def analisar_texto(texto, tipo="url"):
    texto = texto.strip()
    if tipo == "url":
        return analisar_url(texto)
    elif tipo == "email":
        return analisar_email(texto)
    else:
        return {"suspicious": True, "reason": "Tipo de entrada não reconhecido"}
    
def analisar_url(url):
    heuristicas = []

    palavras_suspeitas = carregar_lista("wordlist.txt")
    tlds_suspeitos = carregar_lista("tlds_suspeitos.txt")
    encurtadores = carregar_lista("encurtadores.txt")

    try:
        parsed = urlparse(url)
        dominio = parsed.netloc.lower()

        # 1. Palavras-chave na URL completa
        if any(p in url.lower() for p in palavras_suspeitas):
            heuristicas.append("Contém palavras-chave suspeitas")

        # 2. TLDs suspeito
        if any(dominio.endswith(tld) for tld in tlds_suspeitos):
            heuristicas.append("Domínio de nível superior (TLD) suspeito")

        # 3. Domínio recente
        try:
            info = whois.whois(dominio)
            if info and info.creation_date:
                # Tratamento para data, o whois pode retornar a data como lista, string ou datetime
                criacao = info.creation_date[0] if isinstance(info.creation_date, list) else info.creation_date
                if isinstance(criacao, str):
                    criacao = datetime.strftime(criacao, "%Y-%m-%d %H:%M:%S")

                dias = (datetime.now() - criacao).days
                if dias < 180:
                    heuristicas.append(f"Domínio registrado recentemente ({dias} dias)")
        except whois.parser.PywhoisError:
            heuristicas.append("Falha na consulta WHOIS")
        except Exception:
            heuristicas.append("Erro ao processar a data WHOIS")

        # 4. Encurtadores de URL
        if dominio in encurtadores:
            heuristicas.append("URL encurtada detectada")
            expandida = expandir_url(url)
            if expandida and expandida != url:
                heuristicas.append(f"URL expandida: {expandida}")
        else: 
            # 5. URL com muitos parâmetros
            if url.count("?") > 1 or url.count("=") > 3:
                heuristicas.append("URL com muitos parâmetros (chance de ofuscamento)")

        if heuristicas:
            return {"suspicious": True, "reason": "; ".join(heuristicas)}
        else:
            return {"suspicious": False, "reason": "Nenhum indicador de phishing encontrado"}
        
    except Exception:
        return {"suspicious": True, "reason": "Erro ao processar URL"}
    
# Tenta expandir uma URL encurtada    
def expandir_url(url_encurtada):
    try:
        r = requests.head(url_encurtada, allow_redirects=True, timeout=5)
        return r.url
    except requests.exceptions.RequestException:
        return None

# Analisa um e-mail em busca de indicadores de phishing    
def analisar_email(email):
    heuristicas = []
    palavras_suspeitas = carregar_lista("wordlist.txt")

    try:
        partes_email = email.split("@")
        if len(partes_email) != 2:
            raise ValueError("Formato de email inválido")
        
        usuario = partes_email[0].lower()
        dominio = partes_email[1].lower()

        # 1. Domínios incomuns ou gratuitos
        tlds_suspeitos = carregar_lista("tlds_suspeitos.txt")
        if any(dominio.endswith(tld) for tld in tlds_suspeitos):
            heuristicas.append("Domínio de nível superio (TLD) suspeito")
        
        # 2. Nome de usuário suspeito
        if any(p in usuario for p in palavras_suspeitas):
            heuristicas.append("Nome de usuário suspeito")

        if heuristicas:
            return {"suspicious": True, "reason": "; ".join(heuristicas)}
        else:
            return {"suspicious": False, "reason": "Nenhum indicador de phishing encontrado"}
        
    except ValueError:
        return {"suspicious": True, "reason": "Formato de e-mail inválido"}
    except IndexError:
        return {"suspicious": True, "reason": "Formato de e-mail inválido"}