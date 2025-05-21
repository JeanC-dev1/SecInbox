from src import phishing_checker

def test_check_suspect_keywords():
    text = "Clique aqui para atualizar sua conta bancária"
    result = phishing_checker.check_suspect_keywords(text)
    assert result['suspect_keywords'] == ['clique', 'atualizar', 'conta', 'bancária']

def test_check_domain_similarity():
    result = phishing_checker.check_domain_similarity("http://paypall.com")
    assert result['domain'] == "paypall.com"
    assert result['is_similar_to_legit']  # espera ser similar a 'paypal.com'

def test_check_whois():
    result = phishing_checker.check_whois("http://example.com")
    assert 'creation_date' in result
