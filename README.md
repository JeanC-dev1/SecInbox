# SecureInbox CLI

## Descrição

SecureInbox CLI é uma aplicação multiplataforma (Windows e Linux) desenvolvida em Python que permite a verificação rápida de URLs e endereços de e-mail suspeitos diretamente pelo menu de contexto (clique com o botão direito). O sistema verifica se os links ou e-mails são phishing ou estão envolvidos em vazamentos de dados, utilizando APIs públicas como PhishTank e Leak-Lookup.

---

## Funcionalidades

- Análise de URLs e e-mails suspeitos para detecção de phishing.
- Verificação se o e-mail está presente em bancos de dados de vazamento de dados.
- Integração ao menu de contexto do sistema operacional para análise rápida via clique direito.
- Compatível com Windows e Linux.
- Execução em segundo plano, com resultados exibidos via terminal.
- Modularidade para futura expansão, incluindo interface gráfica (PySide6).

---

## Tecnologias Utilizadas

- Python 3.12
- Bibliotecas: `requests`, `whois`, `python-dotenv`
- APIs públicas: [PhishTank](https://phishtank.org/), [Leak-Lookup](https://leak-lookup.com/)
- Integração ao sistema operacional via arquivos `.reg` (Windows) e scripts `.sh` (Linux)

---

## Como Usar

### Instalação

1. Clone este repositório:

```bash
git clone https://github.com/seu-usuario/SecureInbox.git
cd SecureInbox/src
```

2. Crie um ambiente virtual e ative-o

- Linux/MacOS:

```bash
python3 -m venv venv    
source venv/bin/activate
```

-Windown(PowerShell):

```bash
python3 -m venv venv
.\venv\Scripts\Activate.ps1
```

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

### Execução manual

Para analisar um link ou e-mail, execute: 

```bash
python main.py exemplo@exemplo.com
```
