from server.phishing_checker import *

def test_url_segura():
    """Testa uma URL que deve ser considerada segura."""
    url = "https://www.google.com"
    resultado = analisar_texto(url, tipo="url")
    assert resultado["suspicious"] is False
    assert "Nenhum indicador" in resultado["reason"]

def test_url_suspeita_palavra_chave():
    """Testa uma URL com uma palavra-chave suspeita."""
    url = "https://www.banco-falso.com/login"
    resultado = analisar_texto(url, tipo="url")
    assert resultado["suspicious"] is True
    assert "Contém palavras-chave suspeitas" in resultado["reason"]

def test_url_com_tld_suspeito():
    """Testa uma URL com um TLD (domínio de nível superior) suspeito."""
    url = "https://melhor-promo.xyz/oferta"
    resultado = analisar_texto(url, tipo="url")
    assert resultado["suspicious"] is True
    assert "Domínio de nível superior" in resultado["reason"]

def test_email_seguro():
    """Testa um e-mail que deve ser considerado seguro."""
    email = "contato@empresa.com"
    resultado = analisar_texto(email, tipo="email")
    assert resultado["suspicious"] is False
    assert "Nenhum indicador" in resultado["reason"]

def test_email_com_usuario_suspeito():
    """Testa um e-mail com um nome de usuário suspeito."""
    email = "suporte-banco@dominio.com"
    resultado = analisar_texto(email, tipo="email")
    assert resultado["suspicious"] is True
    assert "Nome de usuário suspeito" in resultado["reason"]

def test_entrada_nao_reconhecida():
    """Testa uma entrada que não é URL nem e-mail."""
    entrada = "isso nao e um link"
    resultado = analisar_texto(entrada, tipo="desconhecido")
    assert resultado["suspicious"] is True
    assert "Tipo de entrada não reconhecido" in resultado["reason"]