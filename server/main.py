import os
from flask import Flask
from flask_smorest import Api
from dotenv import load_dotenv

# Importa os Blueprints dos arquivos de rotas
from api.security_checker_routes import blp as SecurityCheckerBlueprint
from api.status_routes import blp as StatusBlueprint

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

app = Flask(__name__)

# Configurações do Flask-Smorest para a documentação
app.config["API_TITLE"] = "API SecureInbox"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.2"
app.config["OPENAPI_URL_PREFIX"] = "/"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

api = Api(app)

# Registra os Blueprints na API
api.register_blueprint(SecurityCheckerBlueprint)
api.register_blueprint(StatusBlueprint)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)