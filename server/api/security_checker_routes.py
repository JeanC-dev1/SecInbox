from flask import jsonify, request
from flask.views import MethodView
from flask_smorest import Blueprint
from phishing_checker import analisar_texto
from schemas import CheckerSchema

# Cria um Blueprint para as rotas de verificação de segurança
blp = Blueprint("SecurityChecker", __name__, url_prefix="/analisar", description="Endpoints para verificação de segurança")

# Endpoint para analisar texto, URLs ou e-mails
@blp.route("/", methods=["POST"])
class AnalisarResource(MethodView):
    @blp.arguments(CheckerSchema)
    def post(self, analise_data):
        input_text = analise_data.get("texto")
        input_type = analise_data.get("tipo")

        if not input_text or not input_type:
            return jsonify({"error": "Campos 'texto' e 'tipo' são obrigatórios."}), 400

        resultado = analisar_texto(input_text, tipo=input_type)
        return jsonify(resultado)