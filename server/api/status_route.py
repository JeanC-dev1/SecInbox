from flask import jsonify
from flask.views import MethodView
from flask_smorest import Blueprint

blp = Blueprint("Status", __name__, url_prefix="/status", description="Endpoints para verificar o status da API")

@blp.route("/")
class StatusResource(MethodView):
    def get(self):
        return jsonify({"status": "online", "message": "API esta funcionando."})