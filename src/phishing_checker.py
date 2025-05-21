import re
import requests
import whois
from urllib.parse import urlparse
from datetime import datetime

def analyze_text(texto, tipo="url"):
    if tipo == "url":
        return analisar_url(texto)
    elif tipo == "email":
        return analisar_email(texto)
    else:
        return {"suspeito": True, "motivo": "Tipo não reconhecido"}

def analisar_url(url):
    url = url.strip()

    heuristicas = []

    # 1. Palavras-chave comuns em phishing
    palavras_suspeitas = ["login", "senha", "verificação", "urgente", "atualização", "banco", "premio"]
    if any(p in url.lower() for p in palavras_suspeitas):
        heuristicas.append("Contém palavras-chave suspeitas")

    # 2. Domínio estranho ou parecido com marcas
    dominios_duvidosos = [".xyz", ".tk", ".ga", ".ml", ".cf"]
    parsed = urlparse(url)
    if any(parsed.netloc.endswith(ext) for ext in dominios_duvidosos):
        heuristicas.append("Domínio de topo suspeito")

    # 3. Link com muitos parâmetros, pode ser camuflado
    if url.count("?") > 1 or url.count("=") > 3:
        heuristicas.append("Link com muitos parâmetros (camuflagem possível)")

    # 4. Domínio criado recentemente (verifica WHOIS)
    try:
        w = whois.whois(parsed.netloc)
        if w.creation_date:
            if isinstance(w.creation_date, list):
                creation = w.creation_date[0]
            else:
                creation = w.creation_date

            dias = (datetime.now() - creation).days
            if dias < 180:
                heuristicas.append(f"Domínio recente: {dias} dias")
    except:
        heuristicas.append("Não foi possível verificar o domínio")

    if heuristicas:
        return {"suspeito": True, "motivo": "; ".join(heuristicas)}
    else:
        return {"suspeito": False}

def analisar_email(email):
    heuristicas = []

    # 1. Domínio personalizado estranho
    dominio = email.split("@")[-1]
    if dominio.endswith(".xyz") or dominio.count("-") > 1:
        heuristicas.append("Domínio de email incomum ou gratuito")

    # 2. Nome de usuário suspeito
    nome = email.split("@")[0]
    if any(p in nome.lower() for p in ["suporte", "verificacao", "atendimento", "premio"]):
        heuristicas.append("Usuário do email sugere engenharia social")

    if heuristicas:
        return {"suspeito": True, "motivo": "; ".join(heuristicas)}
    else:
        return {"suspeito": False}
