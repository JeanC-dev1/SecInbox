import pytest
from src import utils

def test_validar_email():
    assert utils.validar_email("teste@exemplo.com")
    assert not utils.validar_email("email_invalido")

def test_validar_url():
    assert utils.validar_url("http://exemplo.com")
    assert utils.validar_url("https://secure.site.com")
    assert not utils.validar_url("texto aleatório")
