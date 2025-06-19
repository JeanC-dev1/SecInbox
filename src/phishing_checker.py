import os
import re
import requests
import whois
from urllib.parse import urlparse
from datetime import datetime

def carregar_lista(nome_arquivo):
    caminho = os.path.join(os.path.dirname(__file__), "../data", nome_arquivo)
    try:
        with open(caminho, "r", encoding="utf-8") as f:
            return [linha.strip().lower() for linha in f if linha.strip()]
    except FileNotFoundError:
        return []

def analisar_texto(texto, tipo="url"):
    if tipo == "url":
        return analisar_url(texto)
    elif tipo == "email":
        return analisar_email(texto)
    else:
        return {"suspicious": True, "reason": "Unrecognized input type"}

def analisar_url(url):
    url = url.strip()
    heuristics = []

    palavras_suspeitas = carregar_lista("wordlist.txt")
    tlds_suspeitos = carregar_lista("tlds_suspeitos.txt")
    encurtadores = carregar_lista("encurtadores.txt")

    parsed = urlparse(url)
    dominio = parsed.netloc.lower()

    # 1. Palavras-chave
    if any(p in url.lower() for p in palavras_suspeitas):
        heuristics.append("Contains suspicious keywords")

    # 2. TLDs suspeitos
    if any(dominio.endswith(tld) for tld in tlds_suspeitos):
        heuristics.append("Suspicious top-level domain")

    # 3. Muitos parâmetros
    if url.count("?") > 1 or url.count("=") > 3:
        heuristics.append("URL has too many parameters")

    # 4. Domínio recente
    try:
        info = whois.whois(dominio)
        if info.creation_date:
            created = info.creation_date[0] if isinstance(info.creation_date, list) else info.creation_date
            days = (datetime.now() - created).days
            if days < 180:
                heuristics.append(f"Recently registered domain ({days} days old)")
    except:
        heuristics.append("WHOIS lookup failed")

    # 5. Encurtadores
    if dominio in encurtadores:
        heuristics.append("Shortened URL detected")
        expanded = expandir_url(url)
        if expanded and expanded != url:
            heuristics.append(f"Expanded URL: {expanded}")

    return {"suspicious": True, "reason": "; ".join(heuristics)} if heuristics else {"suspicious": False}

def expandir_url(url_encurtada):
    try:
        r = requests.head(url_encurtada, allow_redirects=True, timeout=5)
        return r.url
    except:
        return None

def analisar_email(email):
    heuristics = []
    palavras_suspeitas = carregar_lista("wordlist.txt")
    dominio = email.split("@")[-1]
    usuario = email.split("@")[0]

    if dominio.endswith(".xyz") or dominio.count("-") > 1:
        heuristics.append("Unusual or free domain")

    if any(p in usuario.lower() for p in palavras_suspeitas):
        heuristics.append("Suspicious sender name")

    return {"suspicious": True, "reason": "; ".join(heuristics)} if heuristics else {"suspicious": False}
