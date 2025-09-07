# SecureInbox - API de Análise de Phishing

Este é o componente de backend do projeto SecureInbox, uma API RESTful dedicada a analisar URLs e e-mails para identificar possíveis ameaças de phishing. A API é construída com **Python** e o framework **Flask**, oferecendo endpoints limpos e eficientes para a verificação de segurança.

---

### Funcionalidades

* **Análise de Conteúdo**: Recebe texto (URLs ou e-mails) e o processa usando um conjunto de regras e heurísticas para detectar indicadores de phishing.
* **API Organizada**: A arquitetura modular separa a lógica de verificação das rotas da API, tornando o código mais fácil de entender e manter.
* **Validação de Dados**: Valida os dados de entrada para garantir que as requisições estejam no formato correto antes de serem processadas.

---

### Instalação e Execução

Para rodar o servidor em sua máquina local, siga os passos abaixo. Certifique-se de que você tem o **Python 3.10** ou superior instalado.

1.  Navegue até o diretório `server/` do seu projeto.
2.  Crie um ambiente virtual para isolar as dependências do projeto:
    ```bash
    python3 -m venv venv
    ```
3.  Ative o ambiente virtual:
    * **No Windows:** `venv\Scripts\activate`
    * **No macOS e Linux:** `source venv/bin/activate`
4.  Instale todas as bibliotecas necessárias listadas no arquivo `requirements.txt`:
    ```bash
    pip install -r requirements.txt
    ```
5.  Inicie o servidor Flask:
    ```bash
    python3 main.py
    ```
O servidor estará rodando em `http://localhost:5000`.

---

### Endpoints da API

A API oferece os seguintes endpoints para interação:

| Endpoint | Método HTTP | Descrição |
| :--- | :--- | :--- |
| `/analisar/` | `POST` | Recebe um texto e seu tipo (`"url"` ou `"email"`) para análise de segurança. |
| `/status/` | `GET` | Retorna o status do servidor, indicando se a API está online e funcional. |

#### **Exemplo de Uso**

Você pode testar a rota `/analisar/` enviando uma requisição `POST` com o tipo e o texto a ser verificado.

**Requisição (URL):**
```bash
curl -X POST \
  http://localhost:5000/analisar/ \
  -H "Content-Type: application/json" \
  -d '{
    "texto": "[http://site-suspeito.com.br](http://site-suspeito.com.br)",
    "tipo": "url"
  }'
```

**Resposta:**
```bash
{
    "suspicious": true,
    "reason": "Indicador de phishing encontrado."
}
```